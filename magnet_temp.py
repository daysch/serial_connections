magtemp_serial_port = 'COM1' # will have to change, most probably

# Python program magnet_temp.py

import serial
import time
from helpers import rec_response

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
sendstring = 'KRDG?\r'
ser.flushInput()
ser.flushOutput()
ser.write(sendstring)
temperature = rec_response(ser)
ser.close()

print temperature

timeseconds=time.time()
timestring=time.ctime(timeseconds)

# Append level and time/date to log file.
logfile=open('magnet_temp.txt','a')
logfile.write(timestring+': '+temperature+'K\n')
logfile.close()