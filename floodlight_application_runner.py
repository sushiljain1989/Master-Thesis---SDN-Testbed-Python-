import sys
import subprocess
import shlex
import os
import shutil
import time
class floodlight_application_runner:

	def runApp(self , applicationName , config):
		self.home = config['home']
		self.old_file = ""
		new_file = ""
		trace = 0
		filePath = config['home']+"/src/main/resources/floodlightdefault.properties"
		applicationNameLower = applicationName.split(".")[0].lower()
		self.applicationNameLower = applicationNameLower
		f = open(filePath , "r")
		for line in f.readlines():
       			 self.old_file = self.old_file+line
       			 if line.startswith('net.floodlightcontroller.statistics.StatisticsCollector') and trace < 1:
               	 		trace+=1
                		line = line.strip() + ",net.floodlightcontroller."+applicationNameLower+"."+applicationName.split(".")[0]+"\n"
        		 new_file += line
		#print new_file
		f.close()
		os.remove(filePath)
		myFile = open(filePath , "w" , 0)
		myFile.write(new_file)
		myFile.close()
		#exit(0)
		os.chdir(config['home']+"/src/main/java/net/floodlightcontroller")
		os.mkdir(applicationNameLower , 0755)
                shutil.copy('/home/vagrant/python/Master---Thesis/apps/floodlight/'+applicationName , config['home']+'/src/main/java/net/floodlightcontroller/'+applicationNameLower+'/' )
		os.chdir(config['home'])
		compileProcess = subprocess.Popen(["ant" , "run"] , shell=False , stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		while True:
                        output = compileProcess.stdout.readline()
                        if output == '' and compileProcess.poll() is not None:
                               break
                        if output:
                                line =  output.strip()
				if line.endswith("Starting DebugServer on :6655"):
					break
                                
		#time.sleep(1)
                #process = subprocess.Popen("java -jar target/floodlight.jar", shell=False, stdout=subprocess.PIPE)
                time.sleep(1)

	def stopApp(self):
		#print "stopping application"
		filePath = self.home+"/src/main/resources/floodlightdefault.properties"
		os.remove(filePath)
		myFile = open(filePath, "w" , 0)
		myFile.write(self.old_file)
		myFile.close()
		shutil.rmtree(self.home+"/src/main/java/net/floodlightcontroller/"+self.applicationNameLower+"/")
		
