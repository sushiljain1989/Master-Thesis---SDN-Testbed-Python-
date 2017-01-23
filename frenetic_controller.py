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
		print self.process.pid
		self.process.kill()
		subprocess.Popen(["freeport" , self.port], shell=False, stdout=subprocess.PIPE)

