import sys
from Environment import Environment
from FreneticApplicationRunner import FreneticApplicationRunner
from FreneticController import FreneticController
class FreneticEnvironment(Environment):

    def __init__(self, configFilePath):
        self.controllerName = "frenetic"
        self.mainConfigFile = configFilePath
	self.readConfigFile()


    def stopApplication(self):
        print "stopping application"
        self.apprunner.stopApp()

    def startController(self):
        print "running controller"
        self.freneticcontroller =  FreneticController()
        self.freneticcontroller.runController(self.dictionary)


    def startApplication(self,applicationName):
        print "running application"
        self.apprunner = FreneticApplicationRunner(self.dictionary, Environment.testBedHomePath)
        self.apprunner.runApp(applicationName, self.dictionary, Environment.testBedHomePath)


    def stopController(self):
        print "stopping controller"
        self.freneticcontroller.stopController()


    def setTestBedHome(self, testBedHomePath='/home/vagrant/python/Master---Thesis/'):
        Environment.testBedHomePath = testBedHomePath

    def additionalConfigFile(self, configFilePath=None, configFileName = None):
        if configFilePath==None or configFileName == None:
            raise Exception('Please provide file path and name')
        else:
            print "reading additional config file"
            Environment.configFiles[configFileName] = configFilePath
