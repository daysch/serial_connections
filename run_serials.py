import easygui as e
import traceback
import webbrowser
import os

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=60)
def timed_job():

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
	# if error_collection != "":
	# 	print error_collection
	# 	e.msgbox(error_collection)

	path = os.path.dirname(os.path.abspath(__file__)) # relative directory path
	errfile=open(path+"\\error.txt",'w')
	errfile.write(error_collection)
	errfile.close()
	webbrowser.open(path+"\\error.txt")

sched.start()