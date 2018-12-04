###COMMUNICATIONS HANDLER
import socket as s
import socketserver

class DBIO_Server(socketserver.StreamRequestHandler): #DATABASE I/O SERVER CLASS
													  #USED WITH SOCKETSERVER TO SIMPLIFY SERVER METHOD

	def setup(self, settingsObj, database):
		self.database = database
		self.settingsObj = settingsObj
		pass

	def handle(self):
		# self.rfile is a file-like object created by the handler;
		# we can now use e.g. readline() instead of raw recv() calls
		self.data = self.rfile.readline().strip()
		print("{} wrote:".format(self.client_address[0]))
		print(self.data)
		# Likewise, self.wfile is a file-like object used to write back
		# to the client
		self.wfile.write(self.data.upper())

def openDBIOServer(settingsObj, db):
	with socketserver.TCPServer((settingsObj.get("server_hostname"), settingsObj.get("server_port")), DBIO_Server) as server:
		server.setup(settingsObj, db)
		server.serve_forever()