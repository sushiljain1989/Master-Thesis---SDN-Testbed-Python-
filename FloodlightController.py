import sys
import subprocess
import shlex
import os
import time
from controller import controller
class FloodlightController(controller):

        def runController(self , config):
                self.ip = config['ip']
                self.port = config['port']
                print "running controller at -> "+self.ip + ":" + self.port 
		'''while True:
			if self.check_port(int(config['ip'])) == 0:
				break
			else:
				time.sleep(0.1)
		'''
		#self.process = subprocess.Popen(["frenetic" , "http-controller" , "--verbosity" , "debug"], shell=False, stdout=subprocess.PIPE)
                #time.sleep(10)
                #print self.process.pid



        def stopController(self):
                print "stopping controller"
                #print self.port
                '''cmd = 'lsof -t -i:{0}'.format(self.port)
                #cmd2 = 'lsof -t -i:{0}'.format(41414)
                pid = subprocess.check_output(cmd, shell=True)
                #pid = int(pid)
		#pid2 = subprocess.check_output(cmd2, shell=True)
		#pid2 = int(pid2)
		pid = pid.replace('\n',' ')
                #print pid2
                killcmd = 'kill -9 {0}'.format(pid)
                #killcmd2 = 'kill -9 {0}'.format(pid2)
                os.system(killcmd)
                #os.system(killcmd2)'''
