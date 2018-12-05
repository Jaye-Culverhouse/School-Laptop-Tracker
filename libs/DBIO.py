import time, json

def getCorrectResponse(stations, database, configObj, data):
	
	if data["STATION_NUMBER"] in stations:
		stations["STATION_NUMBER"]+=1
	else:
		stations["STATION_NUMBER"] = 1

	if data["MESSAGE"] != "":		
		stations, database, configObj, data = messageHandle(stations, database, configObj, data)

	if data["REQUEST"] != "":		
		stations, database, configObj, data = requestHandle(stations, database, configObj, data)

	return stations, database, configObj, data


def messageHandle(stations, database, configObj, data):
	message = data["MESSAGE"]
	if message == "ONLINE":
		data = createCommand(data, MESSAGE="OK")
	elif message == "SHUTDOWN":
		stations["STATION_NUMBER"] = -1
		data = createCommand(data, MESSAGE = "OK")
	elif message == "UPDATE":
		data = createCommand(data, REQUEST = "UPDATE")
	elif message == "UPDATEDATA":
		configObj.setAll(data["PAYLOAD"])
		data = createCommand(data, MESSAGE = "OK")
	elif message == "CHECKOUT":
		database = checkItem(database, data["ARGUMENTS"], 0)
		data = createCommand(data, MESSAGE = "OK")
	elif message == "CHECKIN":
		database = checkItem(database, data["ARGUMENTS"], 1)
		data = createCommand(data, MESSAGE = "OK")
	elif message == "HEARTBEAT" or message == "OK":
		data=""
	else:
		raise ValueError("Unknown message recieved")
	return stations, database, configObj, data

def requestHandle(stations, database, configObj, data):
	request = data["REQUEST"]
	if request == "UPDATE":
		data = createCommand(data, MESSAGE="UPDATEDATA", PAYLOAD = json.dumps(
			json.load(open("settings/station{}.json".format(data["STATION_NUMBER"]))))
		)
	elif request == "GETNAME":
		data = createCommand(data, MESSAGE = "DATA", PAYLOAD = checkName(database, data["ARGUMENTS"][0]))
	elif request == "CANCHECK":
		data = createCommand(data, MESSAGE = "DATA", PAYLOAD = checkIfCanCheck(database, data["ARGUMENTS"][0]))
	elif request == "ISCHECKED":
		data = createCommand(data, MESSAGE = "DATA", PAYLOAD = checkIfCheckedIn(database, data["ARGUMENTS"][0]))
	# elif request == "DIE":
	# 	database = checkItem(database, data["ARGUMENTS"], 0)
	# 	data = createCommand(data, MESSAGE = "OK")
	# elif request == "LIVE":
	# 	database = checkItem(database, data["ARGUMENTS"], 1)
	# 	data = createCommand(data, MESSAGE = "OK")
	elif request == "BOOP":
		data = createCommand(data, MESSAGE = "HEARTBEAT", )
	else:
		raise ValueError("Unknown message recieved")
	return stations, database, configObj, data

def createCommand(data, STATION_NUMBER="", COMMAND_ID="", MESSAGE="", REQUEST="", ARGUMENTS=[], PAYLOAD=""):
	# data["STATION_NUMBER"] = STATION_NUMBER
	# data["COMMAND_ID"] = COMMAND_ID
	data["MESSAGE"] = MESSAGE
	data["REQUEST"] = REQUEST
	data["ARGUMENTS"] = ARGUMENTS
	data["PAYLOAD"] = PAYLOAD
	return data

def checkItem(database, arguments, io):
	

def checkIfCheckedIn(database, DID):
	c = database.cursor()
	DID = (DID,)
	c.execute("SELECT checkedin FROM devices WHERE did=?",DID)
	result1 = c.fetchone()[0]
	if result1 != 1:
		c.execute("SELECT uid FROM events WHERE did=? ORDER BY time DESC LIMIT 1", DID)
		result2 = c.fetchone()[0]
	else:
		result2 = ""
	return [result1,result2]

def checkIfCanCheck(database, UID):
	c = database.cursor()
	UID = (UID,)
	c.execute("SELECT cancheckout FROM users WHERE uid=?",UID)
	result = c.fetchone()
	return result

def checkName(database, UID):
	c = database.cursor()
	UID = (UID,)
	c.execute("SELECT fname, sname, mname FROM users WHERE uid=?",UID)
	result = c.fetchone()
	return result