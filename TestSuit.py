import os
import sys


def testsuite():
    frenetic_applications = ['frenetic_frenetic_app.py', 'frenetic_flooding_hub.py']

    frenetic_testCases = { 'test_packets': ['frenetic_learning_switch.py'], 'test_flowrules': frenetic_applications }
    #'test_flowrules': frenetic_applications,
    pyretic_applications = ['hub.py', 'mac_learner.py']

    pyretic_testCases = {'test_flowrules': ['pyretic_hub.py'], 'test_packets': ['pyretic_mac_learner.py']}

    controllers = {"pyretic":pyretic_testCases  ,"frenetic": frenetic_testCases}

    return controllers
