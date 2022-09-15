import tkinter
import threading
from tkinter import ttk

import picamera
from picamera import PiCamera
import time

root = tkinter.Tk()
root.geometry('300x200')
root.title('Button Demo')

preview_on = True

def quit_everything():
    global preview_on
    root.quit()
    preview_on = False
    
def take_picture():
    camera.start_preview()
    time.sleep(5)

    for effect in camera.IMAGE_EFFECTS:
        filename = "image_%s.jpg" % effect
        camera.image_effect = effect
        camera.capture(filename)
        time.sleep(1)
    camera.stop_preview()
    
btn = ttk.Button(
	root,
	text = 'Quit',
	command = quit_everything
)

picBtn = ttk.Button(
	root,
	text = 'SMILE!',
	command = take_picture
)

filterOneBtn = ttk.Button(
	root,
	text = 'Filter 1',
	command = quit_everything
)

filterOneBtn.pack(ipadx = 5, ipady = 2, expand = True)
picBtn.pack(ipadx = 5, ipady = 5, expand = True)
btn.pack(ipadx = 5, ipady = 5, expand = True)

camera = picamera.PiCamera()
camera.preview_fullscreen = False
camera.preview_window = (620, 320, 640, 480)
camera.resolution = (640,480)

def camera_thread_func():
    global preview_on
    camera.start_preview()
    while preview_on:
        continue
    camera.stop_preview()
        

camera_thread = threading.Thread(target=camera_thread_func)
camera_thread.start()

root.mainloop()

