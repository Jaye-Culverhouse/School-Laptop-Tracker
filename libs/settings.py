###SETTINGS HANDLER
import json
from os import path, system

class settingsManager():

	def __init__(self, settingsfile = "settings.json"):
		self.settingsFile = settingsfile
		if(path.isfile(settingsfile)):
			self.loadSettings()
		else:
			system("touch {}".format(settingsfile))
		return None

	def loadSettings(self):
		self.settings = json.load(open(self.settingsFile, 'r'))
		return True

	def saveSettings(self):
		json.dump(self.settings, open(self.settingsFile, 'w'))
		return True

	def setSetting(self, setting, newValue):
		self.settings[setting] = newValue
		return True

	def getSetting(self, setting):
		return self.settings[setting]

	def getAllSettings(self):
		return self.settings