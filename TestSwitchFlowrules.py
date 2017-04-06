import sys
import time
import subprocess
import importlib
import netifaces
import threading
import os
from Test import Test

def threaded(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def bg_f(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return bg_f

def runovsOfctlPeriodically(switchI, logsDir):
                #switchI = "s1"
                #print logsDir
                file_path = "/home/vagrant/python/Master---Thesis/"+switchI+".log"
                sys.exit(-1)
                if os.path.exists(file_path):
                        os.remove(file_path)
                waitTime = 60.0
                spentTime = 0.0
		#implementing multiple switch rules count using thread and ovs-ofctl dump-flows command
		#bgThread = threading.Thread(target=runovsOfctlPeriodically, args=("s1",))
        	#bgThread.daemon = True
        	#bgThread.start()
		#end running individual thread for each switch interface
                while True:
                        if switchI in netifaces.interfaces():
                                process = subprocess.Popen(["sudo ovs-ofctl dump-flows "+switchI+" >  "+file_path], shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                                time.sleep(0.2)
                                spentTime+=0.2
                                if waitTime <= spentTime:
                                        break
                        else:
                                time.sleep(0.01)
class TestSwitchFlowrules(Test):
	
	def __init__(self, testbedpath, config):
		self.testbedname = testbedpath
		self.config = config	

	def result(self):
	
		while True:
			for process in self.processList:
                        	if process.poll() == None:
                                	#print "waiting"
                                	time.sleep(1)
                        	else:
					self.processList.remove(process)
                                	break
			if len(self.processList) <= 0:
				break

		result = {}
		for switchInterfaceName in self.switchesList:
			f = open(self.config['templogsdir']+switchInterfaceName+".log" , "r")
                	#print "file opened"
                	numRules = 0
                	rulesList = []
                	for line in f.readlines():
                        	#print "Line : "+line
                        	if  line.startswith("NXST_FLOW reply"):
                                	rulesList.append(numRules)
                                	numRules = 0
                        	else:
                                	numRules+=1
                	f.close()
			result[switchInterfaceName] = rulesList
                #print "file closed"
                #print result
                return result
		'''count = 0
		while True:
			if self.process.poll() == None:
				time.sleep(1)
			else: 
				break
		f = open(self.testbedname+"my.log" , "r")
                for line in f.readlines():
                	if "New flow (0)" in line:
				count+=1
			
		f.close()
		result = {"flow rules" : count}
		return result'''
		

	def execute(self, proces = None, config = None):
		#self.topoFileName
                #self.nwTopoName
		#print self.config
		print self.topoFileName
		l = self.topoFileName.split("/")
		l.pop(-1)
		l = "/".join(l)
		print "topo path : "+l
		sys.path.insert(0,l)
		module = importlib.import_module(self.nwTopoName)
		topoClass = getattr(module , self.nwTopoName)
		topoObject = topoClass()
		self.switchesList =  topoObject.switches()
		print self.switchesList
		#l = [1,2,2]
		self.processList = []
		for switchInterfaceName in self.switchesList:
        		file_path = self.config['templogsdir']+switchInterfaceName+".log"
                	#sys.exit(-1)
                	if os.path.exists(file_path):
                        	os.remove(file_path)
			#bgThread = threading.Thread(target=runovsOfctlPeriodically , args=(switchInterfaceName,self.config['templogsdir']))
        		#bgThread.daemon = True
        		#bgThread.start()
        		#self.threadsList.append(bgThread)
			process = subprocess.Popen(["for d in $(seq 1 300); do sudo ovs-ofctl dump-flows "+switchInterfaceName+" >> "+self.config['templogsdir']+switchInterfaceName+".log"+"; sleep 0.1; done;"], shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
			self.processList.append(process)




		

		'''self.process = subprocess.Popen(["sudo timeout "+str(self.config['duration'])+" tshark -i lo -d tcp.port=="+self.config['port']+",openflow -V > "+self.testbedname+"my.log"],shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                output = self.process.stdout.readline()
		while True: 
                	if output == '' and self.process.poll() is not None:
                                break
                        if output:
                                output.strip()
				break''' 
