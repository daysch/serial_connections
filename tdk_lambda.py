tdklambda_serial_port = 'COM1' # will have to change, most probably

# Python program tdk_lambda.py

# Controls TDK Lambda power supply via csv instructions file
# Takes in command line argument of filename (or filepath and filename if in different folder)
# csv file format: instruction value, sleep time (min)
# Relevant commands: 
#	 PC n (change current to n amps)
#	 PV n (change voltage to n volts)

import serial
import csv
import time
import sys
from helpers import rec_response

# get instructions file
if len(sys.argv) < 2:
	sys.exit("ERROR: please give instructions file as command line argument")
instructions_file = sys.argv[1]

# Create an instance of serial object, set serial parameters for Sumitomo F70L Helium Compressor
ser=serial.Serial()

ser.port=tdklambda_serial_port
ser.baudrate=9600
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=1
ser.timeout=2
ser.xonxoff=0

# initialize connection
ser.open()
sendstring = "ADR 06\r"
ser.flushInput()
ser.flushOutput()
ser.write(sendstring)
rec_response(ser) # delays until response received (= ready for next command)
time.sleep(0.05) # pause to ensure readiness

# turn on power
sendstring = "OUT 1\r"
ser.flushInput()
ser.flushOutput()
ser.write(sendstring)
rec_response(ser)

# open instructions file
instr_file = open(instructions_file)
instrs = csv.reader(instr_file)

# perform actions: 
for instruction in instrs:
	# pause to ensure readiness
	time.sleep(0.05)
	# send command
	print "next command:"
	sendstring = instruction[0]+'\r'
	print sendstring
	ser.flushInput()
	ser.flushOutput()
	ser.write(sendstring)
	
	# receive and print response
	print "response:"
	response = rec_response(ser)
	print response

	# delay specified time
	print "waiting ", instruction[1]," minute(s)...\n"
	time.sleep(float(instruction[1])*60)

# turn off remote control
sendstring = "RMT 0\r"
ser.flushInput()
ser.flushOutput()
ser.write(sendstring)

# close connection
ser.close()

## options to change current and/or voltage
# sendstring = "PC 5\r"
# ser.flushInput()
# ser.flushOutput()
# ser.write(sendstring)
# response = ser.read(2) # "OK\r"

# sendstring = "PV 0.05\r"
# ser.flushInput()
# ser.flushOutput()
# ser.write(sendstring)
# response = ser.read(2) # "OK\r"

## query for status
# sendstring = "MC?\r"
# ser.flushInput()
# ser.flushOutput()
# ser.write(sendstring)
# response = ser.read(6)