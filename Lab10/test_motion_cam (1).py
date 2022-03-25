import RPi.GPIO as GPIO
import time
from picamera import PiCamera

camera = PiCamera()
sensor = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)

current_state = 0
time.sleep(0.1)
#current_state = GPIO.input(sensor)

while True:
    if current_state == 1:
        print("Motion Detected")
        camera.start_preview(alpha=200)
        camera.capture('picture.jpg')
        time.sleep(1)
        camera.stop_preview()
        break
    else:
        print("No motion detected so far")
        current_state = GPIO.input(sensor)
#camera.close()     
