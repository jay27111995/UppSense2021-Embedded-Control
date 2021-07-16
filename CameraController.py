# Date: 15th July 2021
# Author: Jayendra Ellamathy 

import numpy as np
from pyzbar import pyzbar
import cv2

from uuid import UUID 


CAMERA_DEBUG = 0 # Turn on to view debug prints 

# Function captures image from camera and decodes the QR code 
# In addition, it checks if the QR code corresponds to a valid BLE UUID destination 
def captureAndDecodeQR(): 
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
    
        # Change to b&w
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Decode barcodes in image 
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes: 

            # Check for QR codes ONLY 
            if barcode.type != 'QRCODE': 
                continue  

            barcodeData = barcode.data.decode("utf-8")

            # Check if the decoded text is a valid UUID or not 
            try: 
                UUID(barcodeData)
            except ValueError: 
                continue
    
            # If we get a valid QR code then cleanup and exit  
            QRCodeReader = barcodeData
            
            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()
            return barcodeData  
        
        if CAMERA_DEBUG == 1: 
            # Display the frame 
            cv2.imshow("Barcode Reader", frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    
# Test function  
def camControllerTest(): 
    QRCodeText = captureAndDecodeQR()
    print(QRCodeText)

