import sys
import subprocess
import shlex
import os
import shutil
import time
from ApplicationRunner import ApplicationRunner
from controller import controller
class KineticApplicationRunner(ApplicationRunner):

        def __init__(self, config, testBedHomePath):
        	self.config = config
        	self.testbedhome = testBedHomePath

	def runApp(self , applicationName , config, testbedhome):
                #os.chdir(self.testbedhome+"apps/kinetic/")
                shutil.copy(self.config['appsdir']+applicationName , self.config['home']+'/pyretic/kinetic/apps')
		os.chdir(self.config['home'])
		process = subprocess.Popen(["pyretic.py" , "-m" , "p0" , "pyretic.kinetic.apps."+applicationName.split(".")[0] ], shell=False, stdout=subprocess.PIPE)
                while True:
                        if controller.checkPort(int(self.config['port'])) == 0:
                                break
                        else:
                                time.sleep(0.1)
		#time.sleep(2)
		#out, err = process.communicate(commands)
                #print out


        def stopApp(self):
                print "stopping application"
                time.sleep(int(self.config['duration']))
		try:
                        cmd = 'lsof -t -i:{0}'.format(self.config['port'])

                        pid = subprocess.check_output(cmd, shell=True)
                        pid = int(pid)
                        killcmd = 'sudo kill -9 {0}'.format(pid)
                        os.system(killcmd)

                        cmd2 = 'lsof -t -i:{0}'.format(41414)
                        pid2 = subprocess.check_output(cmd2, shell=True)
                        pid2 = pid2.replace('\n',' ')
                        killcmd2 = 'sudo kill -9 {0}'.format(pid2)
                        os.system(killcmd2)
                except subprocess.CalledProcessError, e:
                        print e.output
