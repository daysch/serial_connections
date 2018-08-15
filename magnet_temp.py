import serial
import time
import os
from helpers import rec_response

magtemp_serial_port = 'COM1' # will have to change, most probably
path = os.path.dirname(__file__) # relative directory path

# Python program magnet_temp.py

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

print temperature

timeseconds=time.time()
timestring=time.ctime(timeseconds)

# Append level and time/date to log file.
logfile=open(path+'\\magnet_temp.txt','a')
logfile.write(timestring+': '+temperature+'K\n')
logfile.close()