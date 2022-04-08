# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import RPi.GPIO as GPIO
import io
import os
#import picamera
import logging
import socketserver
from threading import Condition
from http import server
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from sense_hat import SenseHat

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

pin = GPIO.PWM(18,2000)
sense = SenseHat()
#pin.start(4)

#GPIO.output(18, True)
#time.sleep(5)
#print('led on')
        
#HTML page    
PAGE="""\
<!DOCTYPE html>
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>SPYFY Live Feed</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>


<input type="button" value="Go back" onclick="history.back()" class="btn">
<h2> Turn SOS: </h2>
<div>
<a href="/on"><button class="btn" id="onbtn" >On</button></a>
<a href="/off"><button class="btn" id="offbtn">Off</button></a>
</div>


<style>
*{
    background-color:rgb(217,217,217);
    font-family: "Helvetica Neue", Helvetica;
}
a{
    text-decoration: None;
}
.btn{
    border: none;
    border-radius: 4px;
    cursor: pointer;
    padding: 20px 50px;
    font-size: 20px;
    display:block;
    background-color: rgb(222, 193, 155);
}
.btn:hover{
    background-color: brown;
    color: white;
    opacity: 1;
}
.btn:active{
    background-color: grey;
}
#onbtn, #offbtn{
    display: inline;
}
input{
    float: right;
}
</style>



</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command 
            'curl -I http://server-ip-address:port' 
        """
        self.send_response(200)
        self.send_header('Content-type', 'index/html')
        self.end_headers()
        
    def _redirect(self, path):
        try:
            self.send_response(303)
            self.send_header('Content-type', 'index/html')
            self.send_header('Location', path)
            self.end_headers()
        except:
            print('')#catch the dissconnected
        
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        elif self.path=='/on':
            
            pin.start(18)
            #GPIO.output(18, GPIO.HIGH)
            status='SOS is On'
            sense.show_message("SOS is on", text_colour=(255,255,255), back_colour=(255, 0, 0)) #white text color and red color back color
            print('on')
        elif self.path=='/off':
            #GPIO.output(18, GPIO.LOW)
            pin.stop()
            status='SOS is Off'
            print('off')
            
        else:
            self.send_error(404)
            self.end_headers()
            
        self._redirect('/')
        
output = StreamingOutput() #had to leave this here to aviod an "output" error

