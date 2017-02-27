import sys
import subprocess
import shlex
import os
import shutil
from application_runner import application_runner
import time
from controller import controller
class pyretic_application_runner(application_runner):

        def runApp(self , applicationName , config):
                os.chdir("/home/vagrant/python/Master---Thesis/apps/pyretic")
                shutil.copy(applicationName , config['home']+'/pyretic/modules')
		os.chdir(config['home'])
		process = subprocess.Popen(["pyretic.py" , "-m" , "p0" , "pyretic.modules."+applicationName.split(".")[0] ], shell=False, stdout=subprocess.PIPE)
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
