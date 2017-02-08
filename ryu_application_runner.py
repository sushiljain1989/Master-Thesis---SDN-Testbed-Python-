import sys
import subprocess
import shlex
import os
import shutil
import time
class ryu_application_runner:

        def runApp(self , applicationName , config):
                os.chdir("/home/vagrant/python/Master---Thesis/apps/ryu")
                #shutil.copy(applicationName , config['home']+'/pyretic/modules')
		#os.chdir(config['home'])
		process = subprocess.Popen(["ryu-manager" , applicationName ], shell=False, stdout=subprocess.PIPE)
                time.sleep(3)
		#out, err = process.communicate(commands)
                #print out


        def stopApp(self):
                print "stopping application"
