import sys
import subprocess
import shlex
import os
import signal
import time
from application_runner import application_runner
class frenetic_application_runner(application_runner):

	def runApp(self , applicationName , config, testbedhome):
		os.chdir(testbedhome+"apps/frenetic/")
		print os.getcwd()
		print applicationName
		self.process = subprocess.Popen(["python" , applicationName], shell=False, stdout=subprocess.PIPE , preexec_fn=os.setsid)
		#out, err = process.communicate(commands)
		#print out
		#self.process = process
		

	def stopApp(self):
		print "waiting 60 seconds before stopping application"
		time.sleep(10)
		os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
		time.sleep(2)
