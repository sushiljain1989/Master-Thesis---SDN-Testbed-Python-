import sys
import subprocess
import shlex
import os
import shutil
import time
class pyretic_application_runner:

        def runApp(self , applicationName , config):
                os.chdir("/home/vagrant/python/Master---Thesis/apps/pyretic")
                shutil.copy(applicationName , config['home']+'/pyretic/modules')
		os.chdir(config['home'])
		process = subprocess.Popen(["pyretic.py" , "-m" , "p0" , "pyretic.modules."+applicationName.split(".")[0] ], shell=False, stdout=subprocess.PIPE)
                time.sleep(3)
		#out, err = process.communicate(commands)
                #print out


        def stopApp(self):
                print "stopping application"
