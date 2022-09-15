import tkinter
import threading
from tkinter import ttk

import picamera

root = tkinter.Tk()
root.geometry('300x200')
root.title('Button Demo')

preview_on = True

def quit_everything():
    global preview_on
    root.quit()
    preview_on = False
    
btn = ttk.Button(
	root,
	text = 'Quit',
	command = quit_everything
)

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

