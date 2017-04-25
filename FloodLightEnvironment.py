import sys
from Environment import Environment
from FloodlightApplicationRunner import FloodlightApplicationRunner
from FloodlightController import FloodlightController
class FloodLightEnvironment(Environment):

    def __init__(self, configFilePath):
        self.controllerName = "floodlight"
        self.mainConfigFile = configFilePath
	self.readConfigFile()


    def stopApplication(self):
        print "stopping application"
	self.apprunner.stopApp()


    def startController(self):
        print "running controller"
        self.flcontroller =  FloodlightController()
        self.flcontroller.runController(self.dictionary)


    def startApplication(self, applicationName):
        print "running application"
        self.apprunner = FloodlightApplicationRunner(self.dictionary, Environment.testBedHomePath)
        self.apprunner.setCodeDir("/src/main/java")
	#load floodlightdefault.properties file from user-supplied location
        self.apprunner.setConfigFile(Environment.configFiles['floodlightdefault.properties'])
	#location of module file in floodlight setup
        self.apprunner.setModuleFile(Environment.configFiles['net.floodlightcontroller.core.module.IFloodlightModule'])
	#location of module loader file placed in apps or other directory
        self.apprunner.setTestBedModuleFile(Environment.configFiles['net.floodlightcontroller.core.module.IFloodlightModule'])
        #print self.dictionary
	#print TestCase.testBedHomePath
	self.apprunner.runApp(applicationName, self.dictionary, Environment.testBedHomePath)


    def stopController(self):
        print "stopping controller"
        self.flcontroller.stopController()

    def setTestBedHome(self, testBedHomePath='./'):
        Environment.testBedHomePath = testBedHomePath

    def additionalConfigFile(self, configFilePath=None, configFileName = None):
        if configFilePath==None or configFileName == None:
            raise Exception('Please provide file path and name')
        else:
            print "reading additional config file"
            Environment.configFiles[configFileName] = configFilePath
