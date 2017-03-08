import sys
from TestCase import TestCase
from floodlight_application_runner import floodlight_application_runner
from floodlight_controller import floodlight_controller
class FLTestCase(TestCase):

    def __init__(self, configFilePath):
        TestCase.controllerName = "floodlight"
        TestCase.mainConfigFile = configFilePath


    def stopApplication(self):
        print "stopping application"
	self.apprunner.stopApp()


    def startController(self):
        print "running controller"
        self.flcontroller =  floodlight_controller()
        self.flcontroller.runController(self.dictionary)


    def startApplication(self, applicationName):
        print "running application"
        self.apprunner = floodlight_application_runner(self.dictionary, TestCase.testBedHomePath)
        self.apprunner.setCodeDir("/src/main/java")
	print TestCase.configFiles
	#load floodlightdefault.properties file from user-supplied location
        self.apprunner.setConfigFile(TestCase.configFiles['floodlightdefault.properties'])
	#location of module file in floodlight setup
        self.apprunner.setModuleFile(TestCase.configFiles['net.floodlightcontroller.core.module.IFloodlightModule'])
	#location of module loader file placed in apps or other directory
        self.apprunner.setTestBedModuleFile(TestCase.configFiles['net.floodlightcontroller.core.module.IFloodlightModule'])
        #print self.dictionary
	#print TestCase.testBedHomePath
	self.apprunner.runApp(applicationName, self.dictionary, TestCase.testBedHomePath)


    def stopController(self):
        print "stopping controller"
        self.flcontroller.stopController()

    def setTestBedHome(self, testBedHomePath='./'):
        TestCase.testBedHomePath = testBedHomePath

    def additionalConfigFile(self, configFilePath=None, configFileName = None):
        if configFilePath==None or configFileName == None:
            raise Exception('Please provide file path and name')
        else:
            print "reading additional config file"
            TestCase.configFiles[configFileName] = configFilePath
