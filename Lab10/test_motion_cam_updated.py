import RPi.GPIO as GPIO
import time
from picamera import PiCamera

buzzsensor = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzsensor,GPIO.OUT)
GPIO.setwarnings(False)

camera = PiCamera()
sensor = 11

#GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)

current_state = 0
time.sleep(0.1)
#current_state = GPIO.input(sensor)
pin = GPIO.PWM(4,200)
pin.start(4)

while True:
    if current_state == 1:
        print("Motion Detected")
        camera.start_preview(alpha=200)
        camera.capture('picture.jpg')
        print("image captured")
        pin.ChangeFrequency(20000)
        time.sleep(3)
        camera.stop_preview()
        break
    else:
        print("No motion detected so far")
        current_state = GPIO.input(sensor)
    
#camera.close()
pin.stop()
GPIO.cleanup()
print("Test Passed")