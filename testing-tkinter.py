import tkinter
import threading
from tkinter import ttk

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
    toaddr = 'zkod777@gmail.com'      # To id 
    me = 'teamassembly2022@gmail.com'          # your id
    subject = "RASPI PIC"              # Subject
  
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "test "   
    #msg.attach(MIMEText(text))  
  
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open("image1.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image1.jpg"')   # File name and format name
    msg.attach(part)  
  
    try:  
       #s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(user = 'teamassembly2022@gmail.com', password = '')  # User id & password
       #s.send_message(msg)  
       s.sendmail(me, toaddr, msg.as_string())  
       s.quit()  
    #except:  
    #   print ("Error: unable to send email")    
    except SMTPException as error:  
          print ("Error")                # Exception

def try_send():
    TO = 'teamassembly2022@gmail.com'
    SUBJECT = 'TEST MAIL'
    TEXT = 'Here is a message from python.'

    # Gmail Sign In
    gmail_sender = 'teamassembly2022@gmail.com'
    gmail_passwd = ''

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                    'From: %s' % gmail_sender,
                    'Subject: %s' % SUBJECT,
                    '', TEXT])

try:
    server.sendmail(gmail_sender, [TO], BODY)
    print ('email sent')
except:
    print ('error sending mail')

def take_picture():
    camera.start_preview()
    time.sleep(5)
    
    camera.capture('image1.jpg')
    #try_send()
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

