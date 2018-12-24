'''
   Author: Mr Chanapai Chuadchum 
   Project name:  Autonomouse Robotics vision 
'''
import serial
from nanpy import(ArduinoApi,SerialManager)
'''
from ocrtextout import ocr_msg,pid # OCR text read out function, PID for the process id to kill processing function  
from autocapturefunction import gpid 
from Autonomouscameraman import gpidd
'''
import microgear.client as microgear # microgear unit function for the IoT 
import time   
import logging # logging data 
import csv 
import pandas  # Pandas importer function for the system data transfer 
import os   # Operating system to control the software to open when needed 
sensor1 = 0    # Back sensor of the autonomouse car 
sensor2 = 0    # Front sensor of the autonomouse car 
sensor3 = 0    # Activation sensors for the robot 
  # Data key set function and value 
Data_1_key =  " "
Data_2_value = " "    
try:
   connection = SerialManager()
   motorunit = ArduinoApi(connection=connection) #Connection astrablished 
except:
    print("Motor unit control ")
   # Beacon function input for the positioning of the robot 
try:
    connection1 = SerialManager("/dev/ttyUSB0",115200)  # Serial input of the Third wireless MCU 
    Wmcu = ArduinoApi(connection=connection1) # Connection connected 
except: 
    print("Wireless message reciever MCU connection lost")  

#try:
 #  sensor_msg = serial.Serial("/dev/ttyUSB0",115200)
#except:
#   print("Sensor read message error please check the sensor unit")
   # Backward function for the robot to move back and detect obstable
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      # Authentication to the server 
appid = "Kornbot" 

gearkey = "wBHqON1EtNqlTzu"

gearsecret =  "nt0utSlDrPEOiYOFFfHYJDbEw"

#ser = serial.Serial("/dev/ttyUSB0",38400)

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def connection2(): 
     logging.info("Robotics Networking now operating connected to the system") 

def subscription(topic,message):
    
   logging.info(topic+" "+message)
    

def disconnect():
    
    logging.debug("disconnect is work")

microgear.setalias("VisualStudio")   #Sending the data back to the operator 

microgear.on_connect = connection2

microgear.on_message = subscription

microgear.on_disconnect = disconnect

microgear.subscribe("/Topic")

microgear.connect(False) 
# The Code function for the communication system 
def Backward_active(sensor1,SpeedStart,SpeedEnd,timechange):
      if int(sensor1) >= 50:
             motorunit.analogWrite(6,0)
             motorunit.analogWrite(10,0)
             motorunit.analogWrite(4,0)
             motorunit.analogWrite(3,0)
             motorunit.analogWrite(9,SpeedEnd + 15)  # Backward function with the control speed 
             motorunit.analogWrite(11,SpeedEnd + 15)
             motorunit.analogWrite(2,SpeedEnd + 15)
             motorunit.analogWrite(5,SpeedEnd + 15)
      else:
             #Backward part
             motorunit.analogWrite(6,SpeedStart)     # Roughly 150    
             motorunit.analogWrite(10,SpeedStart)
             motorunit.analogWrite(4,SpeedStart)
             motorunit.analogWrite(3,SpeedStart)
             time.sleep(timechange) # time sleep speed change 0.05
             motorunit.analogWrite(6,SpeedEnd)           # Roughly 127
             motorunit.analogWrite(10,SpeedEnd)
             motorunit.analogWrite(4,SpeedEnd)
             motorunit.analogWrite(3,SpeedEnd)
             #Forward function  
             motorunit.analogWrite(9,0)
             motorunit.analogWrite(11,0)
             motorunit.analogWrite(2,0)
             motorunit.analogWrite(5,0)
    # Forward and detect the obstacle in front 
def Foward_active(sensor1,sensor2,sensor3,SpeedStart,SpeedEnd,timechange,Target): 
       if int(sensor2) >= 600:
             motorunit.analogWrite(6,SpeedEnd)
             motorunit.analogWrite(10,SpeedEnd)
             motorunit.analogWrite(4,SpeedEnd)
             motorunit.analogWrite(3,SpeedEnd)
             motorunit.analogWrite(9,0)
             motorunit.analogWrite(11,0)
             motorunit.analogWrite(2,0)
             motorunit.analogWrite(5,0)


       elif int(sensor2) < 500: 
             #Backward part
             motorunit.analogWrite(6,0)
             motorunit.analogWrite(10,0)
             motorunit.analogWrite(4,0)
             motorunit.analogWrite(3,0)
             motorunit.analogWrite(9,SpeedStart)
             motorunit.analogWrite(11,SpeedStart)
             motorunit.analogWrite(2,SpeedStart)
             motorunit.analogWrite(5,SpeedStart)
             time.sleep(timechange)
             motorunit.analogWrite(6,0)
             motorunit.analogWrite(10,0)
             motorunit.analogWrite(4,0)
             motorunit.analogWrite(3,0)
             motorunit.analogWrite(9,SpeedEnd)
             motorunit.analogWrite(11,SpeedEnd)
             motorunit.analogWrite(2,SpeedEnd)
             motorunit.analogWrite(5,SpeedEnd)

         
       if int(sensor1) >= 50:
                  motorunit.analogWrite(6,0)
                  motorunit.analogWrite(10,0)
                  motorunit.analogWrite(4,0)
                  motorunit.analogWrite(3,0)
                  motorunit.analogWrite(9,SpeedStart)
                  motorunit.analogWrite(11,SpeedStart)
                  motorunit.analogWrite(2,SpeedStart)
                  motorunit.analogWrite(5,SpeedStart)
       elif int(sensor1) < 50: 
                  motorunit.analogWrite(6,0)
                  motorunit.analogWrite(10,0)
                  motorunit.analogWrite(4,0)
                  motorunit.analogWrite(3,0)
                  motorunit.analogWrite(9,0)
                  motorunit.analogWrite(11,0)
                  motorunit.analogWrite(2,0)
                  motorunit.analogWrite(5,0) 
       if  int(sensor3) >= 600:    # Input the sensor from the main signal source 
                  motorunit.analogWrite(6,0)
                  motorunit.analogWrite(10,0)
                  motorunit.analogWrite(4,0)
                  motorunit.analogWrite(3,0)
                  motorunit.analogWrite(9,0)
                  motorunit.analogWrite(11,0)
                  motorunit.analogWrite(2,0)
                  motorunit.analogWrite(5,0)
                  time.sleep(14)  # Waiting for the processing OCR data transfer done   
                  OCRdata = open("OCRdatatransfer.txt","r")   # Open file and read
                  Textout = OCRdata.readline()  # Read from Text and delete too don't forget 
                  DataOCR = Textout.split(",")   # Data split for the text input function  
                  Data_1_key = DataOCR[1]  # data key input  
                  Data_2_value = DataOCR[2] # data value input
       if int(Data_2_value) == Target: 
                  microgear.chat("VisualStudio","Arrived") # Telling the food is ready to serve 
                  time.sleep(0.3)
                  microgear.chat("VisualStudio",Data_1_key)
                  time.sleep(0.3) 
                  microgear.chat("VisualStudio",Data_2_value)
                  time.sleep(0.3)
                  motorunit.analogWrite(6,0)
                  motorunit.analogWrite(10,0)
                  motorunit.analogWrite(4,0)
                  motorunit.analogWrite(3,0)
                  motorunit.analogWrite(9,SpeedStart)
                  motorunit.analogWrite(11,SpeedStart)
                  motorunit.analogWrite(2,SpeedStart)
                  motorunit.analogWrite(5,SpeedStart)
                  time.sleep(timechange)  
                  motorunit.analogWrite(6,0)
                  motorunit.analogWrite(10,0)
                  motorunit.analogWrite(4,0)
                  motorunit.analogWrite(3,0)
                  motorunit.analogWrite(9,SpeedEnd)
                  motorunit.analogWrite(11,SpeedEnd)
                  motorunit.analogWrite(2,SpeedEnd)
                  motorunit.analogWrite(5,SpeedEnd)
                  time.sleep(5)
       elif int(Data_2_value) != Target:    # Compare the data upto the dataget function 
             #Backward part
             motorunit.analogWrite(6,0)
             motorunit.analogWrite(10,0)
             motorunit.analogWrite(4,0)
             motorunit.analogWrite(3,0)
             motorunit.analogWrite(9,SpeedStart)
             motorunit.analogWrite(11,SpeedStart)
             motorunit.analogWrite(2,SpeedStart)
             motorunit.analogWrite(5,SpeedStart)
             time.sleep(timechange)  
             motorunit.analogWrite(6,0)
             motorunit.analogWrite(10,0)
             motorunit.analogWrite(4,0)
             motorunit.analogWrite(3,0)
             motorunit.analogWrite(9,SpeedEnd)
             motorunit.analogWrite(11,SpeedEnd)
             motorunit.analogWrite(2,SpeedEnd)
             motorunit.analogWrite(5,SpeedEnd)

while True:  
       sensor1 = motorunit.analogRead(0)#Sensor 1 functioning for the Back 
       sensor2 = motorunit.analogRead(1)#Sensor 2 functioning for the front
       print("Back sensor detection:")
       print(sensor1)
       print("Front sensor distance :")
       print(sensor2)
       Foward_active(sensor1,sensor2,sensor3,150,130,0.05,4) # Target sensor input 
      
