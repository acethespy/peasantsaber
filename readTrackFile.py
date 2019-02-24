#import pyglet
from pynput import keyboard
from datetime import datetime, timedelta
from ffpyplayer.player import MediaPlayer
import time
import cv2
import numpy as np

fileName = "darude"
player = MediaPlayer("music/" + fileName + ".mp3")
val = ''
end = False
startTime = datetime.now()
array = np.zeros(1000)
fps = 5
length = 1000

f = open("musicTracks/" + fileName + ".txt", "r")
lines = f.read().split('\n')
fps = int(lines[0])
length = int(lines[1])

for i in range(len(lines) - 3):
    num = int(lines[i + 2])
    if num > 0:
        array[i] = num



while val != 'eof' and not end:
    frame, val = player.get_frame()
    index = (int)((datetime.now() - startTime).total_seconds() * fps)
    if index < len(array) and array[index] > 0:
        print(array[index])
        array[index] = 0
    if val != 'eof' and frame is not None:
        img, t = frame
        # display img

print("end")

""""
while 1:
    frame, val = player.get_frame()
    if val == 'eof':
        break
    elif frame is None:
    	time.sleep(0.01)
        print 'not ready'
    else:
        img, t = frame
        print val, t, img
        time.sleep(val) """


"""
song = pyglet.media.load('music/darude.mp3')
song.play()
pyglet.app.run()


"""