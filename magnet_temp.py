import serial
import time
import os
from helpers import rec_response

magtemp_serial_port = "COM7" # may need to change, if serial port number changes
path = os.path.dirname(os.path.abspath(__file__)) # relative directory path

# open serial port
ser=serial.Serial()
ser.port=magtemp_serial_port
ser.baudrate=9600
ser.bytesize=serial.SEVENBITS
ser.parity=serial.PARITY_ODD
ser.stopbits=1
ser.timeout=5
ser.xonxoff=0

# read data
ser.open()
sendstring = "KRDG?\r\n"
ser.flushInput()
ser.flushOutput()
ser.write(sendstring)
temperature = rec_response(ser)
ser.close()

# error check
if temperature == "":
	temperature = "ERROR"

# get time data
timeseconds=time.time()
timestring=time.ctime(timeseconds)

# Append level and time/date to log file.
logfile=open(path+"\\magnet_temp.txt",'a')
logfile.write(timestring+": "+temperature+"K\n")
logfile.close()

# raise error
if temperature == "ERROR":
	raise RuntimeError("unable to communicate with equipment")