import libs.settings
import libs.communication
import sqlite3
import libs.DBIO
from os import path, system
from sys import argv

def main():
	settingsObj = libs.settings.settingsManager("settings/server_Settings.json")
	
	settingsObj = libs.settings.checkBasicSettings(settingsObj) #Makes sure basic settings are set and 
																#prepares settings file for first time run
	if len(argv) == 3:										
		settingsObj.set("server_hostname", argv[1])
		settingsObj.set("server_port", int(argv[2]))				
	settingsObj.save()
	
	# if not path.isfile(settingsObj.get("server_db_name")): #Check if DB exists and try to copy in template if not
	# 	system("cp {} {}".format(settingsObj.get("server_db_template_name"), settingsObj.get("server_db_name")))

	if not path.isfile(settingsObj.get("server_db_name")): #Throw exception if database template not found
		raise ValueError("The database is missing")

	db_connection = sqlite3.connect(settingsObj.get("server_db_name"))

	libs.communication.openDBIOServer(settingsObj, db_connection)

if __name__ == '__main__':
	main()