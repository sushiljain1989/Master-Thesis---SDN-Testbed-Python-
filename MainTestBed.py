import sys
import ConfigParser
import types
import importlib

class MainTestBed():


	def getIPnPort(self,controllerName):

		config = ConfigParser.ConfigParser()
		config.read("config.ini")
		options = config.options(controllerName)
		dictionary = dict()
		for option in options:
			dictionary[option] = config.get(controllerName, option)
		    
		return dictionary

	def getControllerObject(self,controllerName):
		module = importlib.import_module(controllerName+"_controller")
		controllerClass = getattr(module , controllerName+"_controller")
		controllerObject = controllerClass()
		#controllerObject.runController(config["ip"],config["port"])
		return controllerObject

	def getAppRunnerObject(self , controllerName):
		module = importlib.import_module(controllerName+"_application_runner")
		appRunnerClass = getattr(module , controllerName+"_application_runner")
		appRunnerObject = appRunnerClass()
		return appRunnerObject

	def getTopoObject(self, topoName):
		module = importlib.import_module(topoName)
		networkRunnerClass = getattr(module , topoName)
		networkObject = networkRunnerClass()
		return networkObject

	def getTestCaseObject(self , testCaseName):
	
		module = importlib.import_module(testCaseName)
		testCaseClass = getattr(module , testCaseName)
		testCaseObject = testCaseClass()
		return testCaseObject

	def getOutputWriteObject(self , writerName):
		module = importlib.import_module(writerName)
		writeClass = getattr(module , writerName)
		writerObject = writeClass()
		return writerObject

if __name__ == '__main__':
   obj = MainTestBed()
   controllerName = "frenetic"
   applicationName = "demo_app.py"
   networkTopoName = "SimpleTopo"
   testCaseName = "demo_test"
   writerName = "json_writer"
   portnIP = obj.getIPnPort(controllerName)
   
   #start controller
   controllerObject = obj.getControllerObject(controllerName)
   controllerObject.runController(portnIP["ip"],portnIP["port"])
   
   #stop controller
   controllerObject.stopController()
		