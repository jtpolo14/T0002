#!/usr/bin/python

import socket


def connect():
    # create socket obj
    s = socket.socket()

    # get host from socket
    host = socket.gethostname()

    # set the port
    port = 12345

    # connect to host to port
    s.connect((host, port))

    return s

def sendRequest(db, collection, timestamp, payload):

    # connect to server
    conn = connect()

    # send a db insert request
    conn.sendall('01{0}{1}{2}{3}'.format(db, collection, timestamp, payload))

    # print return code
    rc =  conn.recv(1024)

    # close out connection
    conn.close()

    return rc

print sendRequest('db', 'coll', '03/06', 'json data')
