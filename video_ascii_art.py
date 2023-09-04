import cv2
import os
import getpass
import soundfile as sf
import sounddevice as sd

def play_audio(outdata, frames, time, status):
    global audio_data_index
    if audio_data_index + frames > len(audio_data):
        return
    outdata[:, 0] = audio_data[audio_data_index:audio_data_index+frames, 0]
    outdata[:, 1] = audio_data[audio_data_index:audio_data_index+frames, 1]
    audio_data_index += frames

username = getpass.getuser()
path = os.path.join("C:\\Users", username, "Downloads")
Videopath = os.path.join(path, 'VIDEO NAME.ETX')
Audiopath = os.path.join(path, 'AUDIO NAME.ETX')
CHARS = ' .,-_~;=@#$%^*|'
nw = 50

audio_data, sample_rate = sf.read(Audiopath)
audio_data_index = 0
cap = cv2.VideoCapture(Videopath)
frame_skip = 5
print("\x1b[2J", end='')
new_sample_rate = int(sample_rate * 0.915)

with sd.OutputStream(callback=play_audio, channels=2, samplerate=new_sample_rate, blocksize=256):
    while audio_data_index < len(audio_data):
        ret, img = cap.read()

        if not ret:
            break

        for _ in range(frame_skip):
            ret, _ = cap.read()
            if not ret:
                break

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        h, w = img.shape
        nh = int(h / w * nw)

        img = cv2.resize(img, (nw * 2, nh))

        for row in img:
            for pixel in row:
                index = int(pixel / 280 * len(CHARS))
                print(CHARS[index], end='')

            print()

        print('\x1b[H', end='')
