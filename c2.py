#!/usr/bin/python

import socket

s = socket.socket()
host = socket.gethostname()
port = 12345

s.connect((host, port))
s.sendall('02')
print s.recv(1024)
s.close()
