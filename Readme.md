<p align="center">
##SYSC3010
## Computer Systems Development Project
# SpyFy: Web-based Surveillance Camera

#### Group L1-G5
#### Tochukwu Iroakazi, 101157104
#### Alina Ahmad, 101111867
#### Raiyan Hasan, 101125753
#### TA: Zein Hajj-Ali				       
#### Date: April 12th, 2022 </p>

# 1. Introduction
				
SpyFy is a web-based surveillance camera system that was designed by our team. This surveillance camera was designed using a Raspberry Pi and PiCamera to provide small business owners or homeowners a web-based Surveillance system at a great cost. This project is easy to install and user-friendly at the same time. There will be three Raspberry Pi’s communicating in this project to monitor the area. One of the cameras will be installed at the Front Door and the other will be installed at the Back Door. The main purpose of these clients is to monitor specific areas and when motion is detected the PiCamera will capture an image and send it over to the Server RPi. The 3 Raspberry Pi’s must be connected to the same network in order to send and receive data. This product is useful for almost everyone living in a home, or for small business owners who would like to have a small security system for safety measures. Having a security system nowadays is extremely vital, as the crime rates and home invasions in neighborhoods continue to rise, installing a security system is the best way to prevent something unfortunate from happening. 

# 2. Hardware Requirement(s):
- Raspberry Pi 4  x3
- SenseHat Display x2
- PIR Motion Sensor x2
- Buzzer  x2
- Connection WiresBreadBoard x2
- Pi Camera x2

# 3. Software Requirement(s):
- 	Please Download the following modules on your Raspberry Pi in order to run the python files   provided in the Lab12 folder on GitHub repository. 
- sudo apt update
- sudo apt upgrade
- **Install the following packages required for the system in the client Raspberry Pi’s:**
- pip install threading
- pip install gpiozero 
- pip install signal 
- pip install socket 
- pip install numpy 
- pip install picamera
- pip install datetime
- pip install logging
- pip install sys
- **Install the following packages required into the Server Raspberry Pi:**
- pip install socket
- pip install datetime
- pip install pyrebase
- pip install secure-smtplib
- pip install email

# 4. Downloading Code from Repository
1. Navigate to the ‘Lab12’ folder in the ‘SYSC3010_L1_G5_Projects’ Repository.
2. Set up all the Raspberry Pi’s using Section 3. Make sure that all of the Raspberry Pi’s are connected to the same network. 
3. Download BackdoorClient.py from Lab12 onto the RPi which is present at the back door. Save this file in a folder and also download livefeed_client.py and save it in the same folder as the client code. 
4. Next, download FrontDoor_Client.py from the same folder onto the second client RPi which is installed at the front door. Download livefeed_client.py and save it in the same folder as the client code. 
5. Start the Server RPi and download Server_Recieve.py and save it in a new Folder. It is important to save this file in a folder because the SQL database will be created and saved in this folder.
6. User-End: Download the GUI folder from Lab12 and make the following changes:
- SpyFy.html: Open up the file on Notepad or Sublime Text and change the “IP address” on lines 21 and 23 to the IP address of your front end and back end RPi.
- Spyfyimages.html: Open up the file on Notepad or Sublime Text and add the details of your firebase network on line 36. You can get this information from firebase > project settings. 
Open the SpyFy.html file with your preferred web browser between Google Chrome or Internet Explorer.
 

# 5. Connecting Hardware:
1. Connect the PiCamera on the Raspberry Pi for both doors: 
2. Get a Pin header installed on the SenseHat to use it as a display for this project and connect the SenseHat to the RPi’s. 
3. Directly connect the Motion Sensor to GPIO pin #4 which is pin 7 on the RPi. Pin #2 for Vcc and pin #6 for the GND terminal of the sensor. 
4. Connect the Buzzer to pin #4 and a free Ground pin for the negative terminal.

# 6. Running the program 
1. Open the back and front door client codes and input the Server RPi IP address as the host variable.
2. Make sure the host variable contains the IP address of the Server inside Server_Recieve.py as well.
3. Run the Server_Recieve.py on the Server and it should print ‘listening’ in the python shell.
4. Once the server is listening, start running the FrontDoor_Client.py and BackdoorClient.py. Once motion is detected at either door, the client code will capture an image and send it over to the Server RPi. The Python Shell for Server will indicate whether an image has been saved in Database and Firebase, also an email is sent to the user. 
5. Every captured image will be saved in the local database. This database can be viewed by opening the folder where the server code is saved. 
6. Open the SpyFy.html file with your preferred web browser between Google Chrome or Internet Explorer (Right click on the file and select open with) to view the web app.
 
 
# 7. Testing Components and Functions
For checking the installation and tests, navigate to the Lab10 folder on the main repository. You will see several files that are designed to ensure that all the tests are running smoothly for components and communication.
1. For testing the communication between the firebase and the client, download the file test_firebase(1).py. The following file is responsible for testing whether an image captured is successfully being sent to the firebase storage or not. When the image is received, you will see a print message validating that the test has been passed.
2. For testing the motion sensor on the Client, download the file test_motion_cam_updated.py. The following file is responsible for checking whether the motion sensor is working or not. It does so by checking if motion has been detected, when it senses something it triggers the camera to take an image. If nothing is being detected, it will print that nothing has been detected. Once it goes over these two cases, the test passes.



