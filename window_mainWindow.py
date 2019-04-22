from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlPassword

import libs.client_cv

from client import settingsObj

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
		QRs = libs.client_cv.readUntilQRFound()
		print(QRs[0].data)

	def __buttonSignOutAction(self):
		pass

	def __buttonExitAction(self):
		global settingsObj
		if self._managementPassword.value == settingsObj.get("MANAGEMENT_PASSWORD"):
			sys.exit()