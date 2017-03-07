from FLTestCase import FLTestCase
from FreneticTestCase import FreneticTestCase
from PyreticTestCase import PyreticTestCase
from KineticTestCase import KineticTestCase
from RyuTestCase import RyuTestCase
from MacLearningTestSuite import MacLearningTestSuite
from test_switch_flowrules import test_switch_flowrules
from test_flowrules import test_flowrules
from test_packets import test_packets
from test_controller_packetin import test_controller_packetin
topoFileName = "/home/vagrant/SimpleTopo.py"
nwTopoName = "SimpleTopo"
testbedpath = "/home/vagrant/python/Master---Thesis/"
case = RyuTestCase("/home/vagrant/python/Master---Thesis/config.ini")
#case.setTopology("/home/vagrant/SimpleTopo.py", "SimpleTopo")
#case.additionalConfigFile("floodlightdefault.properties","/home/vagrant/python/Master---Thesis/apps/floodlight/floodlightdefault.properties")
#case.additionalConfigFile("net.floodlightcontroller.core.module.IFloodlightModule",
#                          "/home/vagrant/python/Master---Thesis/apps/floodlight/net.floodlightcontroller.core.module.IFloodlightModule")
pnip = case.readConfigFile()

case.setTestBedHome(testBedHomePath=testbedpath)

sdntest1 = test_controller_packetin(testbedpath, pnip)
sdntest1.setTopology(topoFileName, nwTopoName)

#sdntest2 = test_switch_flowrules(testbedpath, pnip)
#sdntest2.setTopology(topoFileName, nwTopoName)

suite = MacLearningTestSuite("Hub.py")
suite.addTestCase(case)
#suite.addControllerTest(sdntest1)
suite.addControllerTest(sdntest1)
suite.run()
