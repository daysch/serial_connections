import easygui as e
import traceback
error_collection = ""

# read equipment
try:
	import water_chiller
except:
	error_collection += "Failed to read water chiller status:\n\n"+traceback.format_exc()

try:
	import helium_compressor
except:
	error_collection += "Failed to read helium compressor status:\n\n"+traceback.format_exc()

try:
	import magnet_temp
except:
	error_collection += "Failed to read magnet temperature:\n\n"+traceback.format_exc()

# declare errors if appropriate
if error_collection != "":
	print error_collection
	e.msgbox(error_collection)