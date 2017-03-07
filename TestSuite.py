import sys
from TestCase import  TestCase
from test import test
class TestSuite():

    def __init__(self, applicationName):
        self.applicationName = applicationName
        self.testCaseList = []
        self.controllerTestList = []


    def addTestCase(self , testCase):
        if not isinstance(testCase, TestCase):
            raise Exception('Please provide instance of TestCase')
        else:
            self.testCaseList.append(testCase)

    def addControllerTest(self , SDNTest):
        if not isinstance(SDNTest, test):
            raise Exception('Please provide instance of test class/subclass')
        else:
            self.controllerTestList.append(SDNTest)

    def run(self ):
            pass

