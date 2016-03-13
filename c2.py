#!/usr/bin/python

import socket
import datetime
import time
import pytz
import threading


def send_request(sym):
    s = socket.socket()
    host = socket.gethostname()
    port = 12345

    s.connect((host, port))
    print sym
    s.sendall('02{0}'.format(sym))
    print s.recv(1024)
    s.close()


def next_dt(dt, mins):
    nsecs = dt.minute*60 + dt.second + dt.microsecond *1e-6
    delta = (nsecs//mins)*mins + mins - nsecs
    return dt + datetime.timedelta(seconds=delta)


def test(sym):
    print sym


if __name__ == '__main__':

    nd = 900
    next_run = None
    ticker = open('tickers.txt')
    while 1:
        if next_run != next_dt(datetime.datetime.now(pytz.utc), nd):
            next_run = next_dt(datetime.datetime.now(pytz.utc), nd)
            delay = (next_run - datetime.datetime.now(pytz.utc)).total_seconds()
            threading.Timer(delay, lambda: send_request(ticker.readline().split()[0])).start()
            print next_run, delay
        
        #sleep for 5 mins
        time.sleep(nd/2)
