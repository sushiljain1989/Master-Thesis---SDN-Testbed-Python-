import sys
from Environment import Environment
from RyuApplicationRunner import RyuApplicationRunner
from RyuController import RyuController
class RyuEnvironment(Environment):

    def __init__(self, configFilePath):
        Environment.controllerName = "ryu"
        Environment.mainConfigFile = configFilePath


    def stopApplication(self):
        print "stopping application"
	self.apprunner.stopApp()


    def startController(self):
        print "running controller"
        self.ryucontroller =  RyuController()
        self.ryucontroller.runController(self.dictionary)


    def startApplication(self, applicationName):
        print "running application"
        self.apprunner = RyuApplicationRunner(self.dictionary, Environment.testBedHomePath)
        #self.apprunner.setCodeDir("/src/main/java")
        #self.apprunner.setConfigFile("/home/vagrant/python/Master---Thesis/apps/floodlight/floodlightdefault.properties")
        #self.apprunner.setModuleFile("CHANGE")
        #self.apprunner.setTestBedModuleFile("CHANGE")
        #print self.dictionary
	#print TestCase.testBedHomePath
	self.apprunner.runApp(applicationName, self.dictionary, Environment.testBedHomePath)


    def stopController(self):
        print "stopping controller"
        self.ryucontroller.stopController()

    def setTestBedHome(self, testBedHomePath='/home/vagrant/python/Master---Thesis/'):
        Environment.testBedHomePath = testBedHomePath

    def additionalConfigFile(self, configFilePath=None, configFileName = None):
        if configFilePath==None or configFileName == None:
            raise Exception('Please provide file path and name')
        else:
            print "reading additional config file"
            Environment.configFiles[configFileName] = configFilePath
