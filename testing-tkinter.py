import tkinter
import threading
from tkinter import ttk

#https://www.delftstack.com/howto/python/mimemultipart-python/
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders  

import picamera
from picamera import PiCamera
import time

import smtplib

root = tkinter.Tk()
root.geometry('300x200')
root.title('Button Demo')

preview_on = True

camera = picamera.PiCamera()
camera.preview_fullscreen = False
camera.preview_window = (620, 320, 640, 480)
camera.resolution = (640,480)
camera.image_effect = "none"

def quit_everything():
    global preview_on
    root.quit()
    preview_on = False

def send_an_email():  
    toaddr = 'zkod777@gmail.com'
    subject = 'TEST PI PICS'

    # Gmail Sign In
    gmail_sender = 'teamassembly2022@gmail.com'
    gmail_passwd = 'pwyjogittqqadvgk'
  
    msg = MIMEMultipart()  #MIMEMultipart supports use of many content types (texts/images withint HTML)
    msg['Subject'] = subject  
    msg['From'] = gmail_sender  
    msg['To'] = toaddr  
    msg.preamble = "test "   
  
    part = MIMEBase('application', "octet-stream")  #MIMEBase used as base class
    part.set_payload(open("image1.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image1.jpg"')   # File name and format name
    msg.attach(part)
  
    try:  
       s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(gmail_sender, gmail_passwd)  # User id & password
       s.sendmail(gmail_sender, toaddr, msg.as_string())  
       s.quit()      
    except SMTPException as error:  
          print ("Error")                # Exception

def take_picture():
    camera.start_preview()
    time.sleep(5)
    
    camera.capture('image1.jpg')
    send_an_email()
    #camera.stop_preview()

    """
    for effect in camera.IMAGE_EFFECTS:
        filename = "image_%s.jpg" % effect
        camera.image_effect = effect
        camera.capture(filename)
        time.sleep(1)
    camera.stop_preview()
    """

def select_filter(option):
    effect = ['none', 'negative', 'sketch', 'denoise', 'emboss', 'hatch', 'gpen',
              'pastel', 'watercolor', 'film', 'blur', 'saturation', 'colorswap',
              'washedout', 'posterise', 'colorpoint', 'colorbalance', 'cartoon',
              'deinterlace1', 'deinterlace2', 'oilpaint', 'solarize']
    camera.image_effect = effect[int(option)]

btn = ttk.Button(
	root,
	text = 'Quit',
	command = quit_everything
)

picBtn = ttk.Button(root,text = 'SMILE!', command = take_picture)
filterOneBtn = ttk.Button(root, text = 'Filter', command = lambda:select_filter(21))
clearBtn = ttk.Button(root, text = 'Clear', command = lambda:select_filter(0))

clearBtn.pack(ipadx = 5, ipady = 2, expand = True)
filterOneBtn.pack(ipadx = 5, ipady = 2, expand = True)
picBtn.pack(ipadx = 5, ipady = 5, expand = True)
btn.pack(ipadx = 5, ipady = 5, expand = True)

def camera_thread_func():
    global preview_on
    camera.start_preview()
    while preview_on:
        continue
    camera.stop_preview()
        

camera_thread = threading.Thread(target=camera_thread_func)
camera_thread.start()

root.mainloop()

