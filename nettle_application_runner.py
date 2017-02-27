import sys
import subprocess
import shlex
import os
import shutil
import time
class nettle_application_runner:

        def runApp(self , applicationName , config):
                os.chdir("/home/vagrant/python/Master---Thesis/apps/nettle")
                shutil.copy(applicationName , config['home'])
		os.chdir(config['home'])
		process = subprocess.Popen(["stack" , "runghc"  , applicationName ], shell=False, stdout=subprocess.PIPE)
                time.sleep(3)
		#out, err = process.communicate(commands)
                #print out


        def stopApp(self):
                print "stopping application"
