import sys
import json
from abc import ABCMeta, abstractmethod
class DataWriter:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def write(self , result):
		pass
