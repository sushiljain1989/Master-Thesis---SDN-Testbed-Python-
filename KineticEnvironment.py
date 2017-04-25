import sys
from Environment import Environment
from KineticApplicationRunner import KineticApplicationRunner
from KineticController import KineticController
class KineticEnvironment(Environment):

    def __init__(self, configFilePath):
        self.controllerName = "kinetic"
        Environment.mainConfigFile = configFilePath
	self.readConfigFile()


    def stopApplication(self):
        print "stopping application"
	self.apprunner.stopApp()


    def startController(self):
        print "running controller"
        self.kineticcontroller =  KineticController()
        self.kineticcontroller.runController(self.dictionary)


    def startApplication(self, applicationName):
        print "running application"
        self.apprunner = KineticApplicationRunner(self.dictionary, Environment.testBedHomePath)
        #self.apprunner.setCodeDir("/src/main/java")
        #self.apprunner.setConfigFile("/home/vagrant/python/Master---Thesis/apps/floodlight/floodlightdefault.properties")
        #self.apprunner.setModuleFile("CHANGE")
        #self.apprunner.setTestBedModuleFile("CHANGE")
        #print self.dictionary
	#print TestCase.testBedHomePath
	self.apprunner.runApp(applicationName, self.dictionary, Environment.testBedHomePath)


    def stopController(self):
        print "stopping controller"
        self.kineticcontroller.stopController()

    def setTestBedHome(self, testBedHomePath='/home/vagrant/python/Master---Thesis/'):
        Environment.testBedHomePath = testBedHomePath

    def additionalConfigFile(self, configFilePath=None, configFileName = None):
        if configFilePath==None or configFileName == None:
            raise Exception('Please provide file path and name')
        else:
            print "reading additional config file"
            Environment.configFiles[configFileName] = configFilePath
