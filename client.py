import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlPassword
from pyforms import settings as formSettings

formSettings.PYFORMS_STYLESHEET = "css/testcss.css"

import sys
import socket
import json

import libs.client_cv
import libs.DBIO
import libs.settings
import libs.communication


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
	sock = socket.create_connection((settingsObj.get("server_hostname"),settingsObj.get("server_port")))
	sock.sendall(command)	
	recv = sock.recv(4096)
	recv = recv.decode("utf-8")
	recv = json.loads(recv)

	# print(recv)

	stations,database,settingsObj,response = libs.DBIO.getCorrectResponse(stations,database,settingsObj,recv.copy())

	COUNTER = COUNTER+1

	return (response,recv), settingsObj, COUNTER, database, stations

class CheckoutMain(BaseWidget):

	def __init__(self):
		super(CheckoutMain,self).__init__('CheckoutMain')

		self._buttonSignIn = ControlButton("Sign Laptop In")
		self._buttonSignOut = ControlButton("Sign Laptop Out")
		self._buttonExit = ControlButton('Exit')
		self._managementPassword = ControlPassword()
		self.formset = [('_buttonSignIn', '_buttonSignOut'), ('_managementPassword', '_buttonExit')]
		self._buttonExit.value = self.__buttonExitAction
		self._buttonSignIn.value = self.__buttonSignInAction
		self._buttonSignOut.value = self.__buttonSignOutAction

	def __buttonSignInAction(self):
		pass
		QRs = libs.client_cv.readUntilQRFound()
		print(QRs[0].data)

	def __buttonSignOutAction(self):
		pass

	def __buttonExitAction(self):
		if self._managementPassword.value == settingsObj.get("MANAGEMENT_PASSWORD"):
			sys.exit()

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
