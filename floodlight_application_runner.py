import sys
import subprocess
import shlex
import os
import shutil
import time
from application_runner import application_runner
from controller import controller
class floodlight_application_runner(application_runner):

	configFilePath = "apps/floodlight/floodlightdefault.properties"
	modulesFilePath = "/src/main/resources/META-INF/services/"
	moduleFile = "net.floodlightcontroller.core.module.IFloodlightModule"
	codeDir = "/src/main/java"
	configFile = "apps/floodlight/floodlightdefault.properties"
	def runApp(self , applicationName , config, testbedhome):
		self.home = config['home']
		self.testbedhome = testbedhome
		#configFile = "/home/vagrant/python/Master---Thesis/apps/floodlight/floodlightdefault.properties"
        	#modulesFilePath = "/src/main/resources/META-INF/services/"
        	#moduleFile = "net.floodlightcontroller.core.module.IFloodlightModule"
        	#codeDir = "/src/main/java"
		
		'''self.old_file = ""
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
		os.chdir(config['home'])'''
		#read application file to find package name
		packageName = ""
		f = open(self.testbedhome+"apps/floodlight/"+applicationName , "r")
                for line in f.readlines():
                         if line.startswith('package') :
                                packageName = line.split()[1]
				break
                f.close()

		directory = packageName.split(".")
		self.f = ""
		os.chdir(config['home']+floodlight_application_runner.codeDir)
		for folder in directory:
			#print config['home']+codeDir+"/"+folder
			if os.path.isdir(config['home']+floodlight_application_runner.codeDir+self.f+"/"+folder) == True:
				self.f = self.f + "/" + folder
				os.chdir(config['home']+floodlight_application_runner.codeDir+self.f+"/")
			else:
				if folder.endswith(";"):
					folder = folder[:-1]
					
				os.makedirs(config['home']+floodlight_application_runner.codeDir+self.f+"/"+folder)
				self.f = self.f + "/" + folder
				os.chdir(config['home']+floodlight_application_runner.codeDir+self.f+"/")
			
		shutil.copy(self.testbedhome+'apps/floodlight/'+applicationName , os.getcwd() )			
		
		file_path = config['home']+floodlight_application_runner.modulesFilePath+floodlight_application_runner.moduleFile
	        if os.path.exists(file_path):
                        os.rename(file_path , file_path+"_old")	

		shutil.copy(self.testbedhome+'apps/floodlight/'+floodlight_application_runner.moduleFile , config['home']+floodlight_application_runner.modulesFilePath )
		os.chdir(config['home'])
		#compile floodlight and wait
		compileProcess = subprocess.Popen(["ant"] , shell=False , stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		compileProcess.communicate()
		#run foodlight
		runProcess = subprocess.Popen(["java","-jar","target/floodlight.jar","-cf", self.testbedhome+floodlight_application_runner.configFile] , shell=False , stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		#wait until floodlight controller listens on port#6653
		while True:
                        if controller.check_port(int(config['port'])) == 0:
                                break
                        else:
                                time.sleep(0.1)
                

		'''while True:
                        output = compileProcess.stdout.readline()
                        if output == '' and compileProcess.poll() is not None:
                               break
                        if output:
                                line =  output.strip()
				if line.endswith("Starting DebugServer on :6655"):
					break
                '''                
		#time.sleep(1)
                #process = subprocess.Popen("java -jar target/floodlight.jar", shell=False, stdout=subprocess.PIPE)
                time.sleep(1)

	def stopApp(self):
		#print "stopping application"
		#filePath = self.home+"/src/main/resources/floodlightdefault.properties"
		#os.remove(filePath)
		#myFile = open(filePath, "w" , 0)
		#myFile.write(self.old_file)
		#myFile.close()
		file_path = self.home+floodlight_application_runner.modulesFilePath+floodlight_application_runner.moduleFile
                if os.path.exists(file_path):
                        os.remove(file_path)

		if os.path.exists(file_path+"_old"):
                        os.rename(file_path+"_old" , file_path)
		shutil.rmtree(self.home+floodlight_application_runner.codeDir+self.f)
		
