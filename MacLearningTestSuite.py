import sys
from TestSuite import TestSuite
from test import test
class MacLearningTestSuite(TestSuite):

    def __init__(self, applicationName):
        TestSuite.__init__(self, applicationName)

    def run(self):
        print "running MacLearning Test"

        for sdnTest in self.controllerTestList:
            sdnTest.execute()

            for testCase in self.testCaseList:
                testCase.runTestCase(self.applicationName)

            print sdnTest.result()
