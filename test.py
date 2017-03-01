from abc import ABCMeta, abstractmethod
import sys
import traceback
class test:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def result(self):
		pass

	@abstractmethod
	def execute(self, testbedname, proces = None, config = None):
		pass
