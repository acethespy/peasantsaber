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

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
    	index = (int)((datetime.now() - startTime).total_seconds() * fps)
    	if key == keyboard.Key.caps_lock:
        	array[index] = 1;
        	print("1")
    	elif key == keyboard.Key.shift:
        	array[index] = 2;
        	print("2")
    	elif key == keyboard.Key.ctrl:
        	array[index] = 3;
        	print("3")
    	elif key == keyboard.Key.alt:
        	array[index] = 4;
        	print("4")
    	elif key == keyboard.Key.shift_r:
        	end = True;
        	file = open("musicTracks/" + fileName + ".txt","w")
        	file.write(str(fps) + "\n")
        	file.write(str(index + 1) + "\n")
        	for i in array[:index + 1]:
        		file.write(str((int)(i)) + "\n")
        	file.close() 
        	print(array[:index+1])

    	print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()



while val != 'eof' and not end:
    frame, val = player.get_frame()
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