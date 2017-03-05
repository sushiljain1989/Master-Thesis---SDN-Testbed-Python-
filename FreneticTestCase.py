import sys
from TestCase import TestCase
from frenetic_application_runner import frenetic_application_runner
from frenetic_controller import frenetic_controller
class FreneticTestCase(TestCase):

    def __init__(self, configFilePath):
        TestCase.controllerName = "frenetic"
        TestCase.mainConfigFile = configFilePath


    def stopApplication(self):
        print "stopping application"
        self.apprunner.stopApp()

    def startController(self):
        print "running controller"
        self.freneticcontroller =  frenetic_controller()
        self.freneticcontroller.runController(self.dictionary)


    def startApplication(self,applicationName):
        print "running application"
        self.apprunner = frenetic_application_runner(self.dictionary, TestCase.testBedHomePath)
        self.apprunner.runApp(applicationName, self.dictionary, TestCase.testBedHomePath)


    def stopController(self):
        print "stopping controller"
        self.freneticcontroller.stopController()


    def setTestBedHome(self, testBedHomePath='/home/vagrant/python/Master---Thesis/'):
        TestCase.testBedHomePath = testBedHomePath

    def additionalConfigFile(self, configFilePath=None, configFileName = None):
        if configFilePath==None or configFileName == None:
            raise Exception('Please provide file path and name')
        else:
            print "reading additional config file"
            TestCase.configFiles[configFileName] = configFilePath
