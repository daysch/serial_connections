chiller_serial_port = 'COM1' # will have to change, most probably

# Python program water_chiller.py

import serial
import time
import crcmod

# Create an instance of serial object, set serial parameters for water chiller
ser=serial.Serial()

ser.port=chiller_serial_port
ser.baudrate=9600
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=1
ser.timeout=5
ser.xonxoff=0

# read data
ser.open()
sendstring = "CA00012000DE".decode("hex")
ser.flushInput()
ser.flushOutput()
ser.write(sendstring)
response = ser.read(9) # 9 = length of response
ser.close()

# evaluate response
response = str(response.encode("hex"))
if len(response) != 18:
	tmp_str = "Unable to collect data"
else:
	tmp_format = int(response[10:12], 16)
	tmp_data = int(int(response[12:16], 16))
	if tmp_format == 0x10 or tmp_format == 0x11:
		tmp_data = tmp_data / 10
	elif tmp_format == 0x20:
		tmp_data = tmp_data / 100
	tmp_str = str(tmp_data)
	
	if tmp_format == 0x01 or tmp_format == 0x11:
		tmp_str = tmp_str + 'C'

timeseconds=time.time()
timestring=time.ctime(timeseconds)

# Append temperature and time/date to log file.
logfile=open('water_chiller.txt','a')
logfile.write(timestring+': , '+tmp_str+'\n')
logfile.close()