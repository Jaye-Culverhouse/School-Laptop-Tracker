import libs.settings
import libs.communication
import sqlite3

def main():
	settingsObj = libs.settings.settingsManager("server_Settings.json")
	
	if not settingsObj.isSet("server_db_name"):
		settingsObj.set("server_db_name", "server_db.db")
		settingsObj.save()

	db_connection = sqlite3.connect(settingsObj.get("server_db_name"))
	

if __name__ == '__main__':
	main()