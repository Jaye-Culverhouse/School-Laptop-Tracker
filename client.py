import pyforms
from pyforms import settings as formSettings
formSettings.PYFORMS_STYLESHEET = "css/testcss.css"

import sys
import socket
import json

import libs.client_cv
import libs.DBIO
import libs.settings
import libs.communication

from window_mainWindow import *

### GLOBAL variables
COUNTER = 0
stations = {}
database = None
settingsObj = None
###End Global Variables

def sendAndRecieve(command, settingsObj, COUNTER, database, stations):
	
	command = libs.DBIO.setCommandSettings(command, settingsObj, COUNTER)
	command = json.dumps(command)
	command = command + "\n\n"
	command = command.encode("utf-8")
	try:
		sock = socket.create_connection((settingsObj.get("server_hostname"),settingsObj.get("server_port")))
		sock.sendall(command)	
	except Exception as e:
		print(e)
		raise RuntimeError("Network Error: Failed to connect to basestation")
	
	try:
		recv = sock.recv(4096)
	except Exception as e:
		print(e)
		raise RuntimeError("Network Error: Did not recieve a response from basestation")
	
	try:
		recv = recv.decode("utf-8")
		recv = json.loads(recv)
	except Exception as e:
		print(e)
		print(recv)
		raise RuntimeError("Response Error: Unable to decode response from basestation")
	# print(recv)

	stations,database,settingsObj,response = libs.DBIO.getCorrectResponse(stations,database,settingsObj,recv.copy())

	COUNTER = COUNTER+1

	return (response,recv), settingsObj, COUNTER, database, stations

def main():

	###initialisation

	global COUNTER, stations, database, settingsObj

	settingsObj = libs.settings.settingsManager("settings/client_Settings.json")
	
	settingsObj = libs.settings.checkBasicSettings(settingsObj)
	settingsObj.save()
	if len(sys.argv) == 3:									
		settingsObj.set("server_hostname", sys.argv[1])
		settingsObj.set("server_port", int(sys.argv[2]))				
	settingsObj.save()

	online = libs.DBIO.createCommand({},MESSAGE="ONLINE")
	response, settingsObj, COUNTER, database, stations = sendAndRecieve(online, settingsObj, COUNTER, database, stations)
	
	update = libs.DBIO.createCommand({}, REQUEST="UPDATE")
	response, settingsObj, COUNTER, database, stations = sendAndRecieve(update, settingsObj, COUNTER, database, stations)
	
	pyforms.start_app(CheckoutMain)

if __name__ == '__main__':
	main()
