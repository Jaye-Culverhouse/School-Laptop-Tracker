###COMMUNICATIONS HANDLER
import socket as s
import socketserver
import json
import DBIO

####global variables, seemingly unavoidable without modifying socketserver
####and i really don't want to do that

stations = {}
database = None
configObj = None

####end of globals

class DBIO_Server(socketserver.StreamRequestHandler): #DATABASE I/O SERVER CLASS
	
	def handle(self):
		self.data = self.rfile.readline().strip()
		try:
			self.data = json.loads(self.data)
		except:
			print("Bad message recieved")

		stations, database, configObj, response = DBIO.getCorrectResponse(stations, database, configObj, data)
		
		self.wfile.write(a)
		pass

def openDBIOServer(settingsObj, db):
	database = db
	configObj = settingsObj
	with socketserver.TCPServer( (settingsObj.get("server_hostname"), settingsObj.get("server_port")), DBIO_Server) as server:
		server.serve_forever()
