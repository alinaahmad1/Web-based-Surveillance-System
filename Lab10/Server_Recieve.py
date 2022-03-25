import socket
import datetime
import os
import pyrebase
from time import sleep
import smtplib, email, os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders


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
db = firebase.database()


# *********************************************** Email parameters *************************************************
subject='Security Alert: A motion has been detected'
bodyText="""\
Hi,
A motion has been detected.
"""
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=465
USERNAME='alinaahmad236@gmail.com'
PASSWORD='alina1234'
RECIEVER_EMAIL='spyfyalert@gmail.com'


HOST = '172.17.70.185'
PORT = 37212
ADDR = (HOST,PORT)
BUFSIZE = 4096
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(ADDR)
serv.listen(5)
print('listening ...')




while True:
  conn, addr = serv.accept()
  print('client connected ... ', addr)
  filename = 'image' + \
    datetime.datetime.now().strftime('%Y-%m-%dT%H.%M.%S.%f') + '.jpg'
  # create and open file for writing:
  myfile = open(filename, 'wb')

  while True:
    data = conn.recv(BUFSIZE)
    if not data: break
    myfile.write(data)
    
  
  myfile.close()
  print('finished writing file: ', filename)
  
  storage.child(filename).put(filename)
  #sending to realtime database
  url = storage.child(filename).get_url(None)
  data = {'img': url}
  db.child("MyImages").push(data)
  
  print("Image sent")
  os.remove(filename)
  print("File Removed")
  sleep(2)  
  conn.close()
  print('client disconnected')
  session=smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
  session.ehlo()
  session.login(USERNAME, PASSWORD)
  session.sendmail(USERNAME, RECIEVER_EMAIL, bodyText)
  session.quit()
  print("Email sent")
  
  print("Test has passed")
