#!/usr/bin/python

import socket
import threading
import traceback
import sys

import clock
import process01 as p1
import process02 as p2

class serverT0001(object):

    def __init__(self, host, port):
        # set host
        self.host = host

        # set the port to run the server on
        self.port = port

        # create a socket obj
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        # var to keep count of the requests 
        self.r_count = 0
        

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            self.r_count += 1
            threading.Thread(target = self.listenToClient, args = (client, address, self.r_count)).start() 


    def listenToClient(self, c, addr, r_count):
        pid = clock.checkin(addr, r_count)

        size = 2
        
        print 'Processing request from', addr
        try:

            # infinite loop to accept request 
            while True:
                
                # get processing code  
                pc = c.recv(size)

                # logic to process request
                if pc == '00':   rc = '999'                
                elif pc == '01': rc = p1.go(c, pid)
                elif pc == '02': rc = p2.go(c, pid)
                else:            rc = '998'
                
                if rc == '999':  pass
                
        except Exception, e:
            print e 
            c.close()
            return False

        finally:
            print clock.checkout(pid)

    def shutdown(self):
        self.sock.close()

if __name__ == "__main__":
    host='' 
    port=12345
    server = serverT0001(host, port)
    server.listen()
