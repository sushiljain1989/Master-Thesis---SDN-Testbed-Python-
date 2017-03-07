from abc import ABCMeta, abstractmethod
import sys
import traceback
import importlib
class test:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def result(self):
		pass

	@abstractmethod
	def execute(self, proces = None, config = None):
		pass

	def setTopology(self, topoFileName, nwTopoName):
        	self.topoFileName = topoFileName
        	self.nwTopoName = nwTopoName
