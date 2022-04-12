'''
Th following code is for the backdoor of of our project. It is designed to take images upon detecting motion and sending it to the server.

Author(s): Raiyan, Tochukwu
'''

from livefeed_client import *
from threading import Thread  
import time
from gpiozero import MotionSensor

import signal
import io
import socket
import numpy as np
import picamera.array
import datetime
import logging
import sys 

import time
from picamera import PiCamera
import schedule


#*******************************Variables and parameter initialization****************************************
logging.basicConfig(level=logging.INFO, format="%(message)s")
LOG = logging.getLogger("capture_motion")

HOST = '172.17.68.22'  #'192.168.2.71'  inpute the ip address
PORT = 37212
HOST_PORT = (HOST,PORT)
BUFSIZE = 4096

interval = 5
motionIsdetected = False
lastCaptureTime = datetime.datetime.now()

GPIO_PIR = 11
#GPIO.setmode(GPIO.BOARD)
pirVal = GPIO.setup(GPIO_PIR, GPIO.IN)


Current_State  = 0
Previous_State = 0

#****************************************Pir and Camera parameters*****************************************************
pir = MotionSensor(4)
camera = PiCamera(resolution='640x480', framerate=24)


def capture_image():
    data= time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(5)
    print(data)
    camera.capture('%s.jpg'%data)
    camera.stop_preview()
    time.sleep(1)
    

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def livefeed(threadname, camera):
#**************************Main operation of the Live Feed*************************************************************
    address = ('', 8000) #initialize the local address with the ip address and port
    server = StreamingServer(address, StreamingHandler) #initialize the server object
    print("%s is running" % threadname)
    server.serve_forever() #start the server display and keep running
    
def detector(threadname, camera):
#**************************Main Loop of Motion Detector**************************************************************
    while True:
        pir.wait_for_motion()   #pir motion sensor function that waits for motion to be detected and returns true if motion is detected
        print("Motion detected!")
        camera.start_preview(fullscreen=False, window = (1250,10,640,480))    #for the motion detection the preview is made not to be full screen and given a definite window specifications
        filename = "/home/pi/Desktop/" + (time.strftime("%y%b%d_%H:%M:%S")) + ".jpg"     #storing the filename in the filename variable which contains the filename we want to give is and the timestamp and is appended with the extention .jpg
        camera.capture(filename)    #captures an image and stores it with the filename
        #pir.wait_for_no_motion()    #check if there is no motion
        camera.stop_preview()   #stops the camera
        
        

        #************************************Starts the Transmission part*************************************************************
        stream = io.BytesIO()   #a variable stream to help convert our image to binary data for transmission compatibility
        camera.capture(stream, format='jpeg', use_video_port=True)    #captures an image
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #starts up the socket for transmission to the server
        client.connect(HOST_PORT)     #connect to the server using the host and port declared above
        connection = client.makefile('wb')      #create a writable byte file where the images would be stored
          
        stream.seek(0)    # rewind the stream and send the image data:
        connection.write(stream.read())   #transmit the image data
        connection.close()      #close the connection
        client.close()      #close the client
        LOG.info('image captured/sent via stream')
          # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        schedule.every().hour.do(capture_image)


try:
  #start recording and outut to the live feed
    camera.start_recording(output, format='mjpeg') #motion_output=outttput)

    #**************************Create two threads**************************************************************
    thread1 = Thread(target=livefeed, args=("Live Feed", camera,)) #thread that runs the Live Feed Function
    thread2 = Thread(target=detector, args=("Motion Detector", camera,)) #thread that runs the motion detector
    
    #start the two threads
    thread1.start()
    thread2.start()
  
except KeyboardInterrupt as e:
    LOG.info("\nreceived KeyboardInterrupt via Ctrl-C")
    pass
finally:
#camera.close()
    LOG.info("\ncamera running")
    LOG.info("detect motion running\n")
