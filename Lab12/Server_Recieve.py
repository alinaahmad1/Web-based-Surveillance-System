
#***********import all necessary libraries**********************************************
import socket
import datetime
import os
import pyrebase
from time import sleep
import smtplib, email
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import sqlite3

#***********************************firebase parameters*******************************************************

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




#***********************Emailing Parameters************************************************************************8

subject='Security Alert: A motion has been detected'
bodyText="""\
Hi,
A motion has been detected at your Door.
"""
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=465 #the smtp port used
USERNAME='alinaahmad236@gmail.com'   #the server raspberry pi email for sending the mail
PASSWORD='alina1234'      #the server email password
RECIEVER_EMAIL='spyfyalert@gmail.com'  #the house owner email or the reciever's email


#***Socket parameters*
HOST = '172.17.68.22'   #the servers Ip adress
PORT = 37212      #the same port
ADDR = (HOST,PORT)
BUFSIZE = 4096
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        #starting up the socket for reception
serv.bind(ADDR)     #binding  the address holding the host and the port 
serv.listen(5)        #waiting to get data
print('listening ...')

i = 1
while True:
  conn, addr = serv.accept()    #accepts client connection
  print('client connected ... ', addr)    #once client connected, print client connected and the binded address
  filename1 = 'image' + datetime.datetime.now().strftime('%Y-%m-%dT%H.%M.%S.%f') + '.jpg'     #to hold the image being received and append it with the timestamp and extention
  # create and open file for writing:
  myfile = open(filename1, 'wb')    #create a writeable file 

#******************loop to actually recieve image data*************************************
  while True:
    data = conn.recv(BUFSIZE) 
    if not data: break
    myfile.write(data)      #this writes the data received to the file opened
    
  
  myfile.close()      #closes the file
  print('finished writing file: ', filename1)
  
  storage.child(filename1).put(filename1)     #sending the file to the firebase database
  url = storage.child(filename1).get_url(None) #gets the url of the image from the storage
  data = {'img': url} #create the data file with the url for from storage
  db.child("My Images").push(data) #upload the file to the realtime database
  print("Image sent")
  
  

  #*******************creating the local database with sqlite****************************************
  image_database = sqlite3.connect("Image_data.db")    #start up the database name 
  data = image_database.cursor()
  
  #creating the table with attributes in the database
  createTable = '''CREATE TABLE IF NOT EXISTS Image (
    Id INTEGER,
    image BLOB,
    DateTime TIMESTAMP);'''
  insertQuery = "INSERT INTO Image VALUES(?, ?, ?);"    #to insert values to the attributes created
  
  data.execute(createTable)   #startes up the table 
  data.execute(insertQuery, (i, filename1, datetime.datetime.now()))    #starts storing the data recieved with accurate numbering and timestamps
  
  i+=1    #increments the numbering by 1
#   #data.execute("INSERT INTO Image Values(:image)", 
#                  {'image': filename1})
  image_database.commit()       #commits the database
  
  print("Image saved to local database")
  sleep(2)
#   os.remove(filename)
#   print("File Removed")
#   sleep(2)  
  conn.close()
  print('client disconnected')

  #**********************to send the email to the house owner*********************
  session=smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)    #starting up the smpt server with the port
  session.ehlo()
  session.login(USERNAME, PASSWORD)     #logging in to the gmail server with the username and password
  session.sendmail(USERNAME, RECIEVER_EMAIL, bodyText)        #sending the mail from sender to reciever with the bodytext
  session.quit()  #close the email
  print("Email sent")
  image_database.close()# close the database.

