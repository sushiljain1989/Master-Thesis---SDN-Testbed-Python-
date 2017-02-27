from abc import ABCMeta, abstractmethod
import sys
import traceback
class application_runner:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def runApp(self , applicationName , config):
		pass	
	
	@abstractmethod
	def stopApp(self):
		pass
