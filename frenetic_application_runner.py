import sys
import subprocess
import shlex
class frenetic_application_runner:

	def runApp(self , applicationName , config):
		commands = '''
			cd /home/vagrant/python/Master---Thesis/apps/frenetic
			python applicationName
			'''

		process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		out, err = process.communicate(commands)
		print out
		

	def stopApp(self):
		print "stopping application"
