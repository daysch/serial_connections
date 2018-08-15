# receives response from serial port until reaches carriage return or no more input
def rec_response(ser):
	response = ser.read(1)
	while response[-1] != '\r':
		old = response
		response = response + ser.read(1)
		if response == old:
			break
	return response