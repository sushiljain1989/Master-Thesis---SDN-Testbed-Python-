import sys
import subprocess
import shlex
class frenetic_controller:

	def runController(self , ip , port):
		print "running controller at -> "+ip + ":" + port
		self.process = subprocess.Popen(["ping" , "yahoo.com"], shell=False, stdout=subprocess.PIPE)
		print self.process.pid
		
		

	def stopController(self):
		print "stopping controller"
		print self.process.pid
		self.process.kill()
