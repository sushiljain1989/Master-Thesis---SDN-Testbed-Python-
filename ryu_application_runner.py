import sys
import subprocess
import shlex
import os
import shutil
import time
from application_runner import application_runner
from controller import controller
class ryu_application_runner(application_runner):

        def runApp(self , applicationName , config, testbedhome):
                os.chdir(testbedhome+"apps/ryu/")
                #shutil.copy(applicationName , config['home']+'/pyretic/modules')
		#os.chdir(config['home'])
		process = subprocess.Popen(["ryu-manager" , applicationName ], shell=False, stdout=subprocess.PIPE)
                #time.sleep(3)
		while True:
                        if controller.check_port(int(config['port'])) == 0:
                                break
                        else:
                                time.sleep(0.1)
		#out, err = process.communicate(commands)
                #print out


        def stopApp(self):
                print "stopping application"
