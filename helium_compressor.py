import serial
import time
import os
from helpers import rec_response

helcomp_serial_port = "COM10" # may need to change, if serial port number changes
path = os.path.dirname(os.path.abspath(__file__)) # relative directory path

# Create an instance of serial object, set serial parameters for Sumitomo F70L Helium Compressor
ser=serial.Serial()
ser.port=helcomp_serial_port
ser.baudrate=9600
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=1
ser.timeout=5
ser.xonxoff=0

# read data
ser.open()
# temperatures
sendstring = "$TEAA4B9\r"
ser.flushInput()
ser.flushOutput()
ser.write(sendstring)
temperatures = rec_response(ser)
time.sleep(0.05) # pause to ensure readiness
if temperatures == "" or temperatures.split(",")[0] == "$???":
	ser.close()
	raise RuntimeError("unable to communicate with equipment (temperature)")
else:
	print temperatures

# pressures 
sendstring = "$PRA95F7\r"
ser.flushInput()
ser.flushOutput()
ser.write(sendstring)
pressures = rec_response(ser)
time.sleep(0.05) # pause to ensure readiness
if pressures == "" or pressures.split(",")[0] == "$???":
	ser.close()
	raise RuntimeError("unable to communicate with equipment (pressure)")
else:
	print pressures


# status 
sendstring = "$STA3504\r"
ser.flushInput()
ser.flushOutput()
ser.write(sendstring)
status = rec_response(ser)
time.sleep(0.05) # pause to ensure readiness
ser.close()

if status == "" or status.split(",")[0] == "$???":
	raise RuntimeError("unable to communicate with equipment (status)")
else:
	print status

# interpret status bytes
if len(status) > 10:
	status = status.split(",")
	status[1] = "{:016b}".format(int(status[1], 16))
	status = ",".join(status)

# Unix time is number of seconds since Jan 1, 1970 UTC.
# time.time() returns local time (5 hr or 18000 sec behind UTC).
# time.timezone returns 18000 (=5 hr in seconds)
# time.ctime(timeseconds) returns human readable date and time (current local time if no argument).
# Excel time is number of days since Jan 1, 1900 local time.
# 18000/86400=5 hr converts UTC to local time.
timeseconds=time.time()
timestring=time.ctime(timeseconds)

# Append level and time/date to log file.
logfile=open(path+"\\helium_compressor.txt",'a')
logfile.write(timestring+": ,"+temperatures+", "+pressures+", "+status+"\n")
logfile.close()

## If you ever want to interpret stuff:
# temperatures = temperatures.split(',')
# if response[1] == "$???":
# 	print "invalid response from compressor"
# 	raise

# hel_discharge_temp = response[2]
# water_out = response[3]
# water_in = response[4]