import sys
import subprocess
import shlex
import os
import shutil
import time
from application_runner import application_runner
from controller import controller
class ryu_application_runner(application_runner):

        def __init__(self, config, testBedHomePath):
       		self.config = config
        	self.testbedhome = testBedHomePath

	def runApp(self , applicationName , config, testbedhome):
                os.chdir(self.config['appsdir'])
		self.process = subprocess.Popen(["ryu-manager" , applicationName ], shell=False, stdout=subprocess.PIPE)
                #time.sleep(3)
		while True:
                        if controller.check_port(int(self.config['port'])) == 0:
                                break
                        else:
                                time.sleep(0.1)
		#out, err = process.communicate(commands)
                #print out


        def stopApp(self):
		time.sleep(int(self.config['duration']))
                print "stopping application"
