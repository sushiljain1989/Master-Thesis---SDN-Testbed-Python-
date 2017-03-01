import sys
import subprocess
import shlex
import os
import shutil
import time
from application_runner import application_runner
from controller import controller
class kinetic_application_runner(application_runner):

        def runApp(self , applicationName , config, testbedhome):
                os.chdir(testbedhome+"apps/kinetic/")
                shutil.copy(applicationName , config['home']+'/pyretic/kinetic/apps')
		os.chdir(config['home'])
		process = subprocess.Popen(["pyretic.py" , "-m" , "p0" , "pyretic.kinetic.apps."+applicationName.split(".")[0] ], shell=False, stdout=subprocess.PIPE)
                while True:
                        if controller.check_port(int(config['port'])) == 0:
                                break
                        else:
                                time.sleep(0.1)
		#time.sleep(3)
		#out, err = process.communicate(commands)
                #print out


        def stopApp(self):
                print "stopping application"
