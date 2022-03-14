from gpiozero import LED
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

#pin = GPIO.PWM(4,200)
#pin.start(4)
GPIO.output(4, True)
GPIO.output(4, True)
