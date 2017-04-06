from abc import ABCMeta, abstractmethod
import sys
import traceback
class ApplicationRunner:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def runApp(self , applicationName , config, testbedhome):
		pass	
	
	@abstractmethod
	def stopApp(self):
		pass
