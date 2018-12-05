import socket
from sys import argv
import json
s = socket.create_connection((argv[1],argv[2]))
print(argv[1],argv[2])
s.sendall(b'{"STATION_NUMBER": 1, "COMMAND_ID": 1, "MESSAGE": "", "REQUEST": "GETNAME", "ARGUMENTS": [0], "PAYLOAD": {"testSetting": 1}}')
s.sendall(b"\n")
print(s.recv(4096))
