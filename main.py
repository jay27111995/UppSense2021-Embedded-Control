from CameraController import captureAndDecodeQR
import subprocess 
import os

MAIN_DEBUG = 1 # 1 to enable debug prints 

Result_types = ('+ve', '-ve') 
Result = Result_types[0] # FIll in the final result here. Now, using a dummy value 


if __name__ == "__main__":
    # Read the QR code and get the UUID for BLE destination device(Smartphone)
    DestinationUUID = captureAndDecodeQR()
    DestinationUUID = DestinationUUID.lower()

    if MAIN_DEBUG == 1:
        print('Info: Destination UUID = ' + DestinationUUID)

    # Run the command to exec. execute BLEController.py 
    # Because BLEController runs on python v2 and other code including this runs on python v3
    cmd = 'sudo python sendResult.py ' + DestinationUUID + ' ' + Result 

    if MAIN_DEBUG == 1:
        print(cmd)

    out = os.system(cmd)
    print(out)
