import RPi.GPIO as GPIO 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
from datetime import datetime
from picamera import PiCamera
from time import sleep
import os

import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyCJL36ZrHrBQOltD9Ge89mPpbkkZ7hhmHQ",
  'authDomain': "test1-7b8aa.firebaseapp.com",
  'databaseURL': "https://test1-7b8aa-default-rtdb.firebaseio.com",
  'projectId': "test1-7b8aa",
  'storageBucket': "test1-7b8aa.appspot.com",
  'messagingSenderId': "1073974951796",
  'appId': "1:1073974951796:web:75781fc564cea2d265b621",
  'measurementId': "G-K6S58R1B2X"    

}

firebase = pyrebase.initialize_app(firebaseConfig)

storage = firebase.storage()

camera = PiCamera()
camera.start_preview()
sleep(5)
camera.capture('/tmp/picture.jpg')
camera.stop_preview()

while True: 
  try:
        print("pushed")
        now = datetime.now()
        dt = now.strftime("%d%m%Y%H:%M:%S")
        name = dt+".jpg"
        camera.capture(name)
        print(name+" saved")
        storage.child(name).put(name)
        print("Image sent")
        os.remove(name)
        print("File Removed")
        sleep(2)
        break    

  except:
        camera.close()
        
print('Test Passed: Image has been sent to Firebase')