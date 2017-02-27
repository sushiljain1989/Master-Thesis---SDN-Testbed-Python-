from abc import ABCMeta, abstractmethod
import sys
import traceback
import socket
class controller:
	__metaclass__ = ABCMeta

	@abstractmethod
	def runController(self , config):
		pass

	@abstractmethod
	def stopController(self):
		pass
	
	@staticmethod
	def check_port(port, ip='127.0.0.1'):
		sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
		sock.settimeout(0.5)
		result = sock.connect_ex((ip,port))
		return result	
