import time

def getCorrectResponse(stations, database, configObj, data):
	if data["STATION_NUMBER"] in stations:
		stations[STATION_NUMBER]+=1
	else:
		stations[STATION_NUMBER] = 1

	if stations["MESSAGE"] != "":		
		stations, database, configObj, data = messageHandle(stations, database, configObj, data)

	if stations["REQUEST"] != "":
		stations, database, configObj, data = requestHandle(stations, database, configObj, data)		

	return stations, database, configObj, data


def messageHandle(stations, database, configObj, data):
	message = data["MESSAGE"]
	if message == "ONLINE":
		