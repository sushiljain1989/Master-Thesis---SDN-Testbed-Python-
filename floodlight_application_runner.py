import sys
import subprocess
import shlex
import os
import shutil
import time
from application_runner import application_runner
from controller import controller


class floodlight_application_runner(application_runner):

    def __init__(self, config, testBedHomePath):
	self.config = config
	self.testbedhome = testBedHomePath

    def setCodeDir(self, codeDir):
        self.codeDir = codeDir

    def setModuleFile(self, moduleFile):
        self.moduleFilePath = self.config['modulefilepath'] #/src/main/resources/META-INF/services/"
        self.moduleFile =  self.config['modulefilename'] #"net.floodlightcontroller.core.module.IFloodlightModule"

    def setConfigFile(self, configFile):
        self.configFile = configFile

    def setTestBedModuleFile(self, testBedModuleFileForFL):
        self.testBedModuleFileForFL = testBedModuleFileForFL

    def runApp(self, applicationName, config, testbedhome):
        self.home = self.config['home']
        # read application file to find package name
        packageName = ""
        f = open(self.config['appsdir'] + applicationName, "r")
        for line in f.readlines():
            if line.startswith('package'):
                packageName = line.split()[1]
                break
        f.close()

        directory = packageName.split(".")
        self.f = ""
        os.chdir(self.config['home'] + self.codeDir)
        for folder in directory:
            # print config['home']+codeDir+"/"+folder
            if os.path.isdir(config['home'] + self.codeDir + self.f + "/" + folder) == True:
                self.f = self.f + "/" + folder
                os.chdir(self.config['home'] + self.codeDir + self.f + "/")
            else:
                if folder.endswith(";"):
                    folder = folder[:-1]

                os.makedirs(self.config['home'] + self.codeDir + self.f + "/" + folder)
                self.f = self.f + "/" + folder
                os.chdir(self.config['home'] + self.codeDir + self.f + "/")

        shutil.copy(self.config['appsdir'] + applicationName, os.getcwd())

        file_path = self.config['home'] + self.moduleFile
        if os.path.exists(file_path):
            os.rename(file_path, file_path + "_old")
	#print "home: "+self.config['home']
	#print "file path: "+self.moduleFilePath
        shutil.copy(self.testBedModuleFileForFL,
                    self.config['home'] + self.moduleFilePath)
        os.chdir(self.config['home'])
        compileProcess = subprocess.Popen(["ant"], shell=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        compileProcess.communicate()
        # run foodlight
        runProcess = subprocess.Popen(["java", "-jar", "target/floodlight.jar", "-cf",
                                       self.configFile], shell=False,
                                      stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        print "executed command java -jar target/floodlight...."
	# wait until floodlight controller listens on port#6653
        while True:
            if controller.check_port(int(self.config['port'])) == 0:
                break
            else:
                time.sleep(0.1)

        time.sleep(1)

    def stopApp(self):
        file_path = self.home + self.moduleFilePath + self.moduleFile
        if os.path.exists(file_path):
            os.remove(file_path)

        if os.path.exists(file_path + "_old"):
            os.rename(file_path + "_old", file_path)
        shutil.rmtree(self.home + self.codeDir + self.f)
