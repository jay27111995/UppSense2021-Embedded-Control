# Date: 12/07/2021
# Author: Jayendra Ellamathy 

from bluepy.btle import Peripheral, Scanner, BTLEException

# Use the same characteristic UUID in the smartphone application 
UPPSENSE_RESULT_CHARACTERISTIC_UUID =  "a5089693-697f-45a7-a229-55d37e1573ee"

BLE_DEBUG = 0 # Use for debug prints 

# Function to connect to the smartphone application via BLE and send a string message. 
# Use the same DestinationDeviceUUID in the smartphone app to advertise via BLE.
def connectAndSendMessage(DestinationDeviceUUID, message):
	
	# Scan for BLE devices with DestinationDeviceUUID
	print "Info: Scanning for device..."	
        scanner = Scanner()
	DeviceAddress = None
	retries = 10
        
        while DeviceAddress is None and retries > 0:
            retries -= 1
            for result in scanner.scan(1.0):
                if result.getValueText(7) == DestinationDeviceUUID:
                        print "Info: Found device with UUID " + DestinationDeviceUUID 
			DeviceAddress = result.addr
                        break

	if DeviceAddress is None:
		print "Error: Could not find device"
                return 
	

        # Connect to device 
        try:
                peripheral = Peripheral(DeviceAddress, "random")
	except BTLEException as btlee:
                print "Error: Could not connect to device"
	        return
	
	print "Info: Connected to device"

        
        # Send the message 
        if BLE_DEBUG == 1: 
            print "DEBUG: Services offered by peripheral:"
            for svc in peripheral.services:
                print str(svc)
    
        service = peripheral.getServiceByUUID(UPPSENSE_RESULT_CHARACTERISTIC_UUID)
        data_char = service.getCharacteristics(UPPSENSE_RESULT_CHARACTERISTIC_UUID)[0]
        data_handle = data_char.getHandle()
	peripheral.writeCharacteristic(data_handle, message, withResponse=True)
        print "Info: Sent message -- " + message 			
		

# Test function 
def BLEControllerTest(): 
    connectAndSendMessage("a5089693-697f-45a7-a229-55d37e1573ee", "Positive")
