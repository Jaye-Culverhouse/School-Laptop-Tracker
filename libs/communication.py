###COMMUNICATIONS HANDLER
import socket as s
import socketserver
import json
import libs.DBIO


####global variables, seemingly unavoidable without modifying socketserver
####and i really don't want to do that

stations = {}
database = None
configObj = None

####end of globals

class DBIO_Server(socketserver.StreamRequestHandler): #DATABASE I/O SERVER CLASS
	
	def handle(self):
		global database
		global configObj
		global stations
		self.data = self.rfile.readline().strip()
		read = self.data
		try:
			self.data = json.loads(self.data)
		except:
			print("Bad message recieved, could not decode JSON command")

		print("RECIEVE: " + read.decode("utf-8"))
		stations, database, configObj, response = libs.DBIO.getCorrectResponse(stations, database, configObj, self.data)
		print("\n\n")
		response = json.dumps(response)
		print("RESPOND: " + response)
		self.wfile.write(response.encode("utf-8"))
		pass

def openDBIOServer(settingsObj, db):
	print("OPENING SERVER ON {}:{}".format(settingsObj.get("server_hostname"),settingsObj.get("server_port")))

	global database
	global configObj

	database = db
	configObj = settingsObj

	with socketserver.TCPServer( (settingsObj.get("server_hostname"), settingsObj.get("server_port")), DBIO_Server) as server:
		server.serve_forever()
