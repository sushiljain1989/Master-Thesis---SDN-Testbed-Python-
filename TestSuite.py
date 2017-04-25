import sys
from Environment import Environment
from Test import Test
from DataWriter import DataWriter
class TestSuite():

    def __init__(self):
        self.testEnvList = []
        self.controllerTestList = []


    def addEnvironment(self , env):
        if not isinstance(env, Environment):
            raise Exception('Please provide instance of Environment')
        else:
            self.testEnvList.append(env)

    def addTestCase(self , SDNTest):
        if not isinstance(SDNTest, Test):
            raise Exception('Please provide instance of test class/subclass')
        else:
            self.controllerTestList.append(SDNTest)

    def run(self ):
            pass


    def setDataFormat(self, writerObject):
	self.writerObject = writerObject
