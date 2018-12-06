import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
import sys

import libs.client_cv
import libs.DBIO
import libs.settings

class CheckoutMain(BaseWidget):

	def __init__(self):
		super(CheckoutMain,self).__init__('CheckoutMain')

		self._buttonSignIn = ControlButton("Sign Laptop In")
		self._buttonSignOut = ControlButton("Sign Laptop Out")
		self._buttonExit = ControlButton('Press this button')

		self._buttonExit.value = self.__buttonExitAction

	def __buttonExitAction(self):
		sys.exit()

def main():

	settingsObj = libs.settings.settingsManager("settings/client_Settings.json")
	
	settingsObj = libs.settings.checkBasicSettings(settingsObj)

	pyforms.start_app(CheckoutMain)

if __name__ == '__main__':
	main()
