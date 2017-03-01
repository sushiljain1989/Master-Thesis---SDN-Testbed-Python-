import os
import sys


def testsuite():
    frenetic_applications = ['frenetic_frenetic_app.py', 'frenetic_flooding_hub.py']

    frenetic_testCases = { 'test_packets': ['frenetic_learning_switch.py'], 'test_flowrules': ['frenetic_learning_switch.py'], 'test_packets_event': ['frenetic_learning_switch.py'], 'test_periodic_flowrules': ['frenetic_learning_switch.py']} #, 'test_flowrules': frenetic_applications }
    #'test_flowrules': frenetic_applications,
    pyretic_applications = ['hub.py', 'mac_learner.py']

    pyretic_testCases = {'test_flowrules': ['pyretic_hub.py'] } #, 'test_packets': ['pyretic_mac_learner.py']}
    floodlight_testCases = {'test_packets': ['floodlight_Hub.java']}
    kinetic_testCases = {'test_flowrules': ['kinetic_kinetic_app.py']}
    ryu_testCases = {'test_flowrules': ['ryu_SimpleSwitch.py']}
    #controllers = {'floodlight':floodlight_testCases, 'ryu':ryu_testCases, 'kinetic':kinetic_testCases}
    controllers = {'frenetic':frenetic_testCases}
    return controllers
