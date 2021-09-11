from CameraController import captureAndDecodeQR
import subprocess 
import os

MAIN_DEBUG = 1 # 1 to enable debug prints 

Result_types = ('Positive', 'Negative') 

# Send Result == 1/0 for -ve/+ve 
def readQRCodeAndSendResult(Result):
    # Read the QR code and get the UUID for BLE destination device(Smartphone)
    DestinationUUID = captureAndDecodeQR()
    DestinationUUID = DestinationUUID.lower()

    if MAIN_DEBUG == 1:
        print('Info: Destination UUID = ' + DestinationUUID)

    # Run the command to exec. execute BLEController.py 
    # Because BLEController runs on python v2 and other code including this runs on python v3
    cmd = 'sudo python sendResult.py ' + DestinationUUID + ' ' + Result_types[Result]

    if MAIN_DEBUG == 1:
        print(cmd)

    out = os.system(cmd)
    print(out)

