import sys
from TestSuite import TestSuite
from Test import Test
from DataWriter import DataWriter
class MacLearningTestSuite(TestSuite):

    def __init__(self):
        TestSuite.__init__(self)

    def run(self):
        print "running MacLearning Test"

        for sdnTest in self.controllerTestList:
            sdnTest.execute()

            for env in self.testEnvList:
                #print testCase
		env.setTopology(sdnTest.topoFileName, sdnTest.nwTopoName)
		env.setupEnvironment()

            print self.writerObject.write(sdnTest.result())
