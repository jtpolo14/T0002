from celery import Celery
import time
from urllib.request import urlopen
import uuid

app = Celery('tasks', broker='redis://35.165.238.44', backend='redis://35.165.238.44')

@app.task
def check_input_file(file_path):
    return file_path

@app.task
def move_input_file(file_path_start, file_path_end):
    return (file_path_start, file_path_end)

@app.task
def word_count_python(infile='readme.txt'):
	start = time.time()
	with open(infile) as reader:
		word_count = 0
		for line in reader:
			word_count += len(line.split())
	time.sleep(5)
	return (word_count, time.time() - start)

@app.task
def a001_get_file(file_url):
	start = time.time()
	ret = get_from_url(file_url)
	if not ret['status'] == 0:
		return ('a001 - error downloading url', time.time() - start)
	else:
		return (ret['file'], time.time() - start)


def get_from_url(url, prefix=None):
	file_name = get_unique_file_name(prefix)
	response = urlopen(url)
	CHUNK = 16 * 1024
	with open(file_name, 'wb') as f:
	    while True:
	        chunk = response.read(CHUNK)
	        if not chunk:
	            break
	        f.write(chunk)
	return {'file':file_name, 'status':0}

def get_unique_file_name(prefix=None):
	if prefix and type(prefix) == str:
		return prefix + str(uuid.uuid4()) 
	else:
		return str(uuid.uuid4())





