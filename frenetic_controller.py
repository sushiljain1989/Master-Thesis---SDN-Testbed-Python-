import sys
import subprocess
import shlex
import os
import time
class frenetic_controller:

	def runController(self , config):
		self.ip = config['ip']
		self.port = config['port']
		print "running controller at -> "+self.ip + ":" + self.port
		self.process = subprocess.Popen(["frenetic" , "http-controller" ], shell=False, stdout=subprocess.PIPE)
		time.sleep(10)
		print self.process.pid
		
		

	def stopController(self):
		print "stopping controller"
        	print self.port
        	cmd = 'lsof -t -i:{0}'.format(self.port)
        	pid = subprocess.check_output(cmd, shell=True)
        	pid = int(pid)
        	print pid
        	killcmd = 'kill -9 {0}'.format(pid)
        	killcmd2 = 'kill -9 {0}'.format(self.process.pid)
        	os.system(killcmd)
        	os.system(killcmd2)
