import libs.settings
import libs.communication
import sqlite3

from os import path, system

def main():
	settingsObj = libs.settings.settingsManager("server_Settings.json")
	
	settingsObj = libs.settings.checkBasicSettings(settingsObj) #Makes sure basic settings are set and 
																#prepares settings file for first time
																#run
	settingsObj.save()
	
	if not path.isfile(settingsObj.get("server_db_name")): #Check if DB exists and try to copy in template if not
		system("cp {} {}".format(settingsObj.get("server_db_template_name"), settingsObj.get("server_db_name")))

	if not path.isfile(settingsObj.get("server_db_name")): #Throw exception if database template not found
		raise ValueError("Could not find {} (database template)".format(settingsObj.get("server_db_template_name")))

	db_connection = sqlite3.connect(settingsObj.get("server_db_name"))

if __name__ == '__main__':
	main()