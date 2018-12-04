###SETTINGS HANDLER
import json

class settingsManager():

	def __init__(self, settingsfile = "serverSettings.json"):
		self.settingsFile = settingsfile
		self.loadSettings()
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