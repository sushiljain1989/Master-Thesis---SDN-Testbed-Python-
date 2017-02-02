import sys
import subprocess
import shlex
import os
import shutil
import time
class kinetic_application_runner:

        def runApp(self , applicationName , config):
                os.chdir("/home/vagrant/python/Master---Thesis/apps/kinetic")
                shutil.copy(applicationName , config['home']+'/pyretic/kinetic/apps')
		os.chdir(config['home'])
		process = subprocess.Popen(["pyretic.py" , "-m" , "p0" , "pyretic.kinetic.apps."+applicationName.split(".")[0] ], shell=False, stdout=subprocess.PIPE)
                time.sleep(3)
		#out, err = process.communicate(commands)
                #print out


        def stopApp(self):
                print "stopping application"
