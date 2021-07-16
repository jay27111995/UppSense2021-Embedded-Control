# Date: 15th July 2021
# Author: Jayendra Ellamathy 

# Usage: python sendResult.py "<DESTINATION UUID>" "<RESULT>"

from BLEController import connectAndSendMessage
import argparse 

SEND_RESULT_DEBUG = 1 

parser = argparse.ArgumentParser()
parser.add_argument("DestinationUUID", type=str)
parser.add_argument("Result", type=str)
args = parser.parse_args()

if SEND_RESULT_DEBUG == 1: 
    print args.DestinationUUID
    print args.Result

connectAndSendMessage(args.DestinationUUID, args.Result)
