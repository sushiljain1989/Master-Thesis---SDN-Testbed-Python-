import sys
import subprocess
import shlex
import os
import signal
import time
from ApplicationRunner import ApplicationRunner
class FreneticApplicationRunner(ApplicationRunner):

	def __init__(self, config, testBedHomePath):
        	self.config = config
        	self.testbedhome = testBedHomePath

	def runApp(self , applicationName , config, testbedhome):
		os.chdir(self.testbedhome+"apps/frenetic/")
		#print os.getcwd()
		#print applicationName
		self.process = subprocess.Popen(["python" , self.config['appsdir']+applicationName], shell=False, stdout=subprocess.PIPE , preexec_fn=os.setsid)
		'''while True:
            		output = self.process.stdout.readline()
            		if output == '' and self.process.poll() is not None:
                		break
            		if output:
                		print output.strip()
                		#break'''
		#time.sleep()
		#out, err = process.communicate(commands)
		#print out
		#self.process = process
		

	def stopApp(self):
		print "waiting 60 seconds before stopping application"
		time.sleep(int(self.config['duration']))
		#time.sleep(10)
		os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
		time.sleep(2)
