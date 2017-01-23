import sys
import subprocess
import shlex
class frenetic_controller:

	def runController(self , ip , port):
		print "running controller at -> "+ip + ":" + port
		self.port = port
		self.process = subprocess.Popen(["frenetic" , "http-controller" , "--verbosity" , "debug"], shell=False, stdout=subprocess.PIPE)
		print self.process.pid
		
		

	def stopController(self):
		print "stopping controller"
        print self.port
        cmd = 'lsof -t -i:{0}'.format(self.port)
        pid = subprocess.check_output(cmd, shell=True)
        pid = int(pid)
        print pid
        killcmd = 'kill -9 {0}'.format(pid)
        killcmd2 = 'kill -9 {0}'.format(self.process.pid)
        os.system(killcmd)
        os.system(killcmd2)
