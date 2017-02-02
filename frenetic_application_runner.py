import sys
import subprocess
import shlex
import os
import signal
import time
class frenetic_application_runner:

	def runApp(self , applicationName , config):
		os.chdir("/home/vagrant/python/Master---Thesis/apps/frenetic")
		print applicationName
		self.process = subprocess.Popen(["python" , applicationName], shell=False, stdout=subprocess.PIPE , preexec_fn=os.setsid)
		#out, err = process.communicate(commands)
		#print out
		#self.process = process
		

	def stopApp(self):
		print "stopping application"
		os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
		time.sleep(2)
