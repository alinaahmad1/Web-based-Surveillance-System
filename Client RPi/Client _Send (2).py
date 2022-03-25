import signal
import io
import socket
import numpy as np
import picamera
import picamera.array
import datetime
import logging
import sys 

import RPi.GPIO as GPIO
import subprocess
import time
import requests
from picamera import PiCamera
import picamera.array
import schedule

logging.basicConfig(level=logging.INFO, format="%(message)s")
LOG = logging.getLogger("capture_motion")

HOST = '172.17.70.185'  #inpute the ip address
PORT = 37212
HOST_PORT = (HOST,PORT)
BUFSIZE = 4096

interval = 5
motionIsdetected = False
lastCaptureTime = datetime.datetime.now()

GPIO_PIR = 11
GPIO.setmode(GPIO.BOARD)
pirVal = GPIO.setup(GPIO_PIR, GPIO.IN)


Current_State  = 0
Previous_State = 0

def capture_image():
    data= time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(5)
    print(data)
    camera.capture('%s.jpg'%data)
    camera.stop_preview()
    time.sleep(1)

# The 'analyse' method gets called on every frame processed while picamera
# is recording h264 video.
# It gets an array (see: "a") of motion vectors from the GPU.
class DetectMotion(picamera.array.PiMotionAnalysis):
  def analyse(self, a):
    global interval, motionIsdetected, lastCaptureTime

    if datetime.datetime.now() > lastCaptureTime + \
        datetime.timedelta(seconds=interval):

      a = np.sqrt(
            np.square(a['x'].astype(np.float64)) +
            np.square(a['y'].astype(np.float64))
            ).clip(0, 255).astype(np.uint8)
    
      if (a > 60).sum() > 10 or pirVal == 1:
        LOG.info('motion detected at: %s' % datetime.datetime.now().strftime('%Y-%m-%dT%H.%M.%S.%f'))
        motionIsdetected = True

camera = picamera.PiCamera()
with DetectMotion(camera) as output:
  try:
    camera.resolution = (640, 480)
    camera.framerate= 10
    # record video to nowhere, as we are just trying to capture images:
    camera.start_recording('/dev/null', format='h264', motion_output=output)
    while True:
      while not motionIsdetected:
        LOG.info('waiting for motion...')
        camera.wait_recording(1)

      LOG.info('stop recording and capture an image...')
      camera.stop_recording()
      motionIsdetected = False
      # Current_State = GPIO.input(GPIO_PIR)
 
      # if Current_State==1 and Previous_State==0:
      #   # PIR is triggered
      #   print('Motion detected!')

      stream = io.BytesIO()
      camera.capture(stream, format='jpeg', use_video_port=True)
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client.connect(HOST_PORT)
      connection = client.makefile('wb')
      # rewind the stream and send the image data:
      stream.seek(0)
      connection.write(stream.read())
      connection.close()
      client.close()
      LOG.info('image captured/sent via stream')
      # Reset the stream for the next capture
      stream.seek(0)
      stream.truncate()

      # record video to nowhere, as we are just trying to capture images:
      camera.start_recording('/dev/null', format='h264', motion_output=output)

      # schedule.every().hour.do(capture_image)
      
      
  except KeyboardInterrupt as e:
    LOG.info("\nreceived KeyboardInterrupt via Ctrl-C")
    pass
  finally:
    camera.close()
    LOG.info("\ncamera turned off!")
    LOG.info("detect motion has ended.\n")
