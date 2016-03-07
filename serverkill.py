import subprocess
p = subprocess.Popen('ps -ax | grep serverT0002.py', stdout=subprocess.PIPE, shell=True)
(out, err)  = p.communicate() 
for t in out.split('\n'):
	if 'python serverT0002.py' in t:
		subprocess.call(['kill', t.split()[0]])
		print 'Terminated: ', t