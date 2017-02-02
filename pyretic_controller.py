import sys
import subprocess
import shlex
import os
import time
class pyretic_controller:

        def runController(self , config):
		self.ip = config['ip']
                self.port = config['port']
                print "running controller at -> "+self.ip + ":" + self.port
                #self.process = subprocess.Popen(["frenetic" , "http-controller" , "--verbosity" , "debug"], shell=False, stdout=subprocess.PIPE)
                #time.sleep(10)
                #print self.process.pid



        def stopController(self):
                print "stopping controller"
                #print self.port
                cmd = 'lsof -t -i:{0}'.format(self.port)
                cmd2 = 'lsof -t -i:{0}'.format(41414)
                pid = subprocess.check_output(cmd, shell=True)
                pid = int(pid)
		pid2 = subprocess.check_output(cmd2, shell=True)
		#pid2 = int(pid2)
		pid2 = pid2.replace('\n',' ')
                print pid2
                killcmd = 'kill -9 {0}'.format(pid)
                killcmd2 = 'kill -9 {0}'.format(pid2)
                os.system(killcmd)
                os.system(killcmd2)
