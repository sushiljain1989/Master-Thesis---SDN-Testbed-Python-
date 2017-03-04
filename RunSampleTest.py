from FLTestCase import FLTestCase
from MacLearningTestSuite import MacLearningTestSuite
from test_flowrules import test_flowrules
testbedpath = "/home/vagrant/python/Master---Thesis/"
case = FLTestCase("config.ini")
case.additionalConfigFile("floodlightdefault.properties","/home/vagrant/python/Master---Thesis/apps/floodlight/floodlightdefault.properties")
case.additionalConfigFile("net.floodlightcontroller.core.module.IFloodlightModule",
                          "/home/vagrant/python/Master---Thesis/apps/floodlight/net.floodlightcontroller.core.module.IFloodlightModule")
pnip = case.readConfigFile("config.ini")

case.setTestBedHome(testBedHomePath=testbedpath)

sdntest = test_flowrules(testbedpath, pnip)

suite = MacLearningTestSuite("MACLearn.java")
suite.addTestCase(case)
suite.addControllerTest(sdntest)
suite.run()
