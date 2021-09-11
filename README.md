Embedded system developed for InfluSense 1.0 - H1N1 Biosensor: developed by UppSense, Uppsala University, Sweden 

UpSense team and project info:
Website: https://sensusuppsala.com/
LinkedIn: https://www.linkedin.com/company/uppsense/mycompany/
Facebook: https://www.facebook.com/UppsalaSensUs
Instagram: https://www.instagram.com/uppsalasensus/ 
Sensus Competition: https://digital.sensus.org/teams/4 

Read team result document in repository for more info. 

Description: 
Platform: RaspberryPI 
HW: Camera, touch-screen display module, peralstatic pumps, servo motors, motor driver extension board, potentiostat from PalmSens  
Authors: Jayendra Ellamathy, Yifan Liu

Features: 
* User-Interface to operate the biosensor: to start measurement, 
send result to user, 
display plot of DPV(Differential Pulse Voltammetry), 
view the camera window to scan QR code. 
UI written using Tkinter, matplotlib.   
* Routine to control the sequence of operation of pumps and valves for the microfluidic system. 
* To scan a QR code containing the BLE(Bluetooth Low Energy) UUID(Universally Unique Identifier) of user's smartphone and send the result. Code to scan the QR code written with openCV. Bluetooth code written with bluepy. For subsequent iOS app code, visit: https://github.com/jay27111995/UppSense-iOS-App-Deveopment

