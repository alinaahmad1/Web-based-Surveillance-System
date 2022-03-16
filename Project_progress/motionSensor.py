import RPi.GPIO as GPIO
import time
from picamera import PiCamera

camera = PiCamera()
sensor = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)

current_state = 0
time.sleep(0.1)
current_state = GPIO.input(sensor)
if current_state == 1:
    print("Motion Detected")
    camera.start_preview()
    camera.capture('/Desktop/picture.jpg')
    time.sleep(1)
    camera.stop_preview()
else:
    print("No motion detected so far")
    camera.stop_preview()

        
    
