###SETTINGS HANDLER
import json
from os import path, system

class settingsManager():

	def __init__(self, settingsfile = "settings.json"):
		self.settingsFile = settingsfile
		if(path.isfile(settingsfile)):
			self.load()
		else:
			system("touch {}".format(settingsfile))
			self.settings = {}
		return None

	def isSet(self, setting):
		return setting in self.settings

	def load(self):
		self.settings = json.load(open(self.settingsFile, 'r'))
		return True

	def save(self):
		json.dump(self.settings, open(self.settingsFile, 'w'))
		return True

	def set(self, setting, newValue):
		self.settings[setting] = newValue
		return True

	def get(self, setting):
		return self.settings[setting]

	def getAll(self):
		return self.settings

	def setAll(self, newJSON):
		for key in newJSON.keys():
			self.settings[key] = newJSON[key]
		self.save()
		return True
		# self.settings = newJSON
		# return True
def checkBasicSettings(settingsObj):
	if not settingsObj.isSet("server_db_name"):
		settingsObj.set("server_db_name", "server_db.db")

	if not settingsObj.isSet("server_db_template_name"):
		settingsObj.set("server_db_template_name", "server_db_template.db")

	if not settingsObj.isSet("server_hostname"):
		settingsObj.set("server_hostname", "localhost")

	if not settingsObj.isSet("server_port"):
		settingsObj.set("server_port", 3141)
	return settingsObj