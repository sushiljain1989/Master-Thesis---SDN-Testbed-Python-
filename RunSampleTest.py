#!/usr/bin/python
from FloodLightEnvironment import FloodLightEnvironment
from FreneticEnvironment import FreneticEnvironment
from PyreticEnvironment import PyreticEnvironment
from KineticEnvironment import KineticEnvironment
from RyuEnvironment import RyuEnvironment
from MacLearningTestSuite import MacLearningTestSuite
from TestSwitchFlowrules import TestSwitchFlowrules
from TestFlowrules import TestFlowrules
from TestPackets import TestPackets
from TestPacketIn import TestPacketIn
from JSONWriter import JSONWriter 
topoFileName = "/home/vagrant/SimpleTopo.py"
nwTopoName = "SimpleTopo"
testbedpath = "/home/vagrant/python/Master---Thesis/"
env = RyuEnvironment("/home/vagrant/python/Master---Thesis/config.ini")
env.setApplication("SimpleSwitch.py")
#env.additionalConfigFile(configFileName="floodlightdefault.properties",configFilePath="/home/vagrant/python/Master---Thesis/apps/floodlight/floodlightdefault.properties")
#env.additionalConfigFile(configFileName="net.floodlightcontroller.core.module.IFloodlightModule",
#                          configFilePath="/home/vagrant/python/Master---Thesis/apps/floodlight/net.floodlightcontroller.core.module.IFloodlightModule")
pnip = env.readConfigFile()

env.setTestBedHome(testBedHomePath=testbedpath)

#sdntest1 = test_controller_packetin(testbedpath, pnip)
#sdntest1.setTopology(topoFileName, nwTopoName)

sdntest2 = TestSwitchFlowrules(testbedpath, pnip)
sdntest2.setTopology(topoFileName, nwTopoName)

outputFormat = JSONWriter()

suite = MacLearningTestSuite()
suite.addTestCase(env)
#suite.addControllerTest(sdntest1)
suite.addControllerTest(sdntest2)
suite.setDataFormat(outputFormat)
suite.run()
