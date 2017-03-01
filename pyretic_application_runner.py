import sys
import subprocess
import shlex
import os
import shutil
from application_runner import application_runner
import time
from controller import controller
class pyretic_application_runner(application_runner):

        def runApp(self , applicationName , config, testbedhome):
		self.port = config['port']
                os.chdir(testbedhome+"apps/pyretic")
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
		try:
                        cmd = 'lsof -t -i:{0}'.format(self.port)

                        pid = subprocess.check_output(cmd, shell=True)
                        pid = int(pid)
                        killcmd = 'kill -9 {0}'.format(pid)
                        os.system(killcmd)

                        cmd2 = 'lsof -t -i:{0}'.format(41414)
                        pid2 = subprocess.check_output(cmd2, shell=True)
                        pid2 = pid2.replace('\n',' ')
                        killcmd2 = 'kill -9 {0}'.format(pid2)
                        os.system(killcmd2)
                except subprocess.CalledProcessError, e:
                        print e.output
