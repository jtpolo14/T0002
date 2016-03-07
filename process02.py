import time

def go(client, pid):
	size = 1024
	rc = '000'
	for x in range(100, 105): 
	    print x
	    time.sleep(5)
	payload = client.recv(size)
	print payload
	# send reply and close connection
	client.send('CC: {0}; {1}'.format(pid, rc))
	client.close()
	return rc