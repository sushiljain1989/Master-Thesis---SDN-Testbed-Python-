import sys
import ConfigParser
import types
import importlib
import subprocess
import os
import time
import pexpect
import signal
import netifaces
import threading
from controller import controller
from application_runner import application_runner
from test import test
def threaded(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def bg_f(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return bg_f

def runovsOfctlPeriodically(switchI):
                #switchI = "s1"
		#print switchI
		file_path = "/home/vagrant/python/Master---Thesis/"+switchI+".log"
		if os.path.exists(file_path):
			os.remove(file_path)
                waitTime = 60.0
                spentTime = 0.0
                while True:
                        if switchI in netifaces.interfaces():
                                process = subprocess.Popen(["sudo ovs-ofctl dump-flows "+switchI+" >> /home/vagrant/python/Master---Thesis/"+switchI+".log"], shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                                time.sleep(0.1)
                                spentTime+=0.1
                                if waitTime <= spentTime:
                                        break
                        else:
                                time.sleep(0.01)

class MainTestBed():


	def getIPnPort(self,controllerName):

		config = ConfigParser.ConfigParser()
		config.read("/home/vagrant/python/Master---Thesis/config.ini")
		options = config.options(controllerName)
		dictionary = dict()
		for option in options:
			dictionary[option] = config.get(controllerName, option)
		    
		return dictionary

	def getControllerObject(self,controllerName):
		module = importlib.import_module(controllerName+"_controller")
		controllerClass = getattr(module , controllerName+"_controller")
		controllerObject = controllerClass()
		#controllerObject.runController(config["ip"],config["port"])
		return controllerObject

	def getAppRunnerObject(self , controllerName):
		module = importlib.import_module(controllerName+"_application_runner")
		appRunnerClass = getattr(module , controllerName+"_application_runner")
		appRunnerObject = appRunnerClass()
		return appRunnerObject
	
	def runMininet(self , topoName , fileName, configs):
		bgThread = threading.Thread(target=runovsOfctlPeriodically , args=("s1",))
                bgThread.daemon = True
                bgThread.start()	
		#print configs
		#fd = sys.stdin.fileno()
		#fl = fcntl.fcntl(fd , fcntl.F_GETFL)
		#fcntl.fcntl(fd , fcntl.F_SETFL , fl | os.O_NONBLOCK)
		process = subprocess.Popen("sudo mn --custom /home/vagrant/python/Master---Thesis/"+fileName+".py --topo="+topoName+" --controller=remote,ip="+configs['ip']+",port="+configs['port'],shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT , preexec_fn=os.setsid)
		#process.expect(pexpect.EOF)
		#stdout,stderr = process.communicate("pingall")
		#print stdout
		#print "stderrrrrrrrrrr"
		#print stderr
		while True:
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				output.strip()
				break
		#print process.poll()
		#thread.daemon = True
		#thread.start()
		'''bgThread.daemon = True
		bgThread.start()'''
		time.sleep(1)
		process.stdin.write("pingall \n")
                process.stdin.flush()
                time.sleep(0.5)
                while True:
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                                break
			if "*** Results" in output.strip():
                                print output.strip()
                                break
		#result = ""
		return process

	def stopMininet(self , process):
		#os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                #time.sleep(1)
		cmd = 'ps -ef | awk \'/[m]n/{print $2}\'' #'lsof -t -i:{0}'.format(self.port)
		pid = subprocess.check_output(cmd, shell=True)
		killcmd2 = 'sudo kill -9 {0}'.format(pid.strip().replace('\n',' '))
		os.system(killcmd2)
		subprocess.Popen("sudo mn -c" , shell=True)
		time.sleep(2)

	def getTopoObject(self, topoName):
		module = importlib.import_module(topoName)
		networkRunnerClass = getattr(module , topoName)
		networkObject = networkRunnerClass()
		return networkObject

	def getTestCaseObject(self , testCaseName):
	
		module = importlib.import_module(testCaseName)
		testCaseClass = getattr(module , testCaseName)
		testCaseObject = testCaseClass()
		return testCaseObject

	def getOutputWriteObject(self , writerName):
		module = importlib.import_module(writerName)
		writeClass = getattr(module , writerName)
		writerObject = writeClass()
		return writerObject

	def generateTraffic(self, mininetProcess):
		runTime = 10
		startTime = 1
		while True:
			if(startTime >= runTime):
				break
			mininetProcess.stdin.write("h1 nc h2 21 \n")
                	mininetProcess.stdin.flush()
			startTime+=1
			time.sleep(1)
		startTime = 1
		print "starting ssh traffic"
		while True:
                        if(startTime >= runTime):
                                break
                        mininetProcess.stdin.write("h1 nc h2 22 \n")
                        mininetProcess.stdin.flush()
                        startTime+=1
                        time.sleep(1)
                startTime = 1
		print "starting mail traffic"
		while True:
                        if(startTime >= runTime):
                                break
                        mininetProcess.stdin.write("h1 nc h2 25 \n")
                        mininetProcess.stdin.flush()
                        startTime+=1
                        time.sleep(1)
                startTime = 1
		print "starting http traffic"
		while True:
                        if(startTime >= runTime):
                                break
                        mininetProcess.stdin.write("h1 nc h2 80 \n")
                        mininetProcess.stdin.flush()
                        startTime+=1
                        time.sleep(1)
                startTime = 1
		print "starting https traffic"
		while True:
                        if(startTime >= runTime):
                                break
                        mininetProcess.stdin.write("h1 nc h2 443 \n")
                        mininetProcess.stdin.flush()
                        startTime+=1
                        time.sleep(1)
	
	#@threaded
'''	def runovsOfctlPeriodically(self, switchI):
		#switchI = "s1"
		waitTime = 60.0
		spentTime = 0.0
                while True:
                        if switchI in netifaces.interfaces():                                
				self.process = subprocess.Popen(["sudo ovs-ofctl dump-flows "+switchI+" >> /home/vagrant/python/Master---Thesis"+switchI+".log"], shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
				time.sleep(0.1)
				spentTime+=0.1
				if waitTime <= spentTime:
					break
			else:
				time.sleep(0.1)	'''

if __name__ == '__main__':
   resultsDict = {}
   
   obj = MainTestBed()
   #print "hello"
   #exit(0)
   #portnIP = obj.getIPnPort(controllerName)
   #controllers = ["nettle","ryu","frenetic" , "pyretic" , "kinetic" , "floodlight"]
   controllers = ["frenetic"]
   applications = ["nettle_Main.hs","ryu_L2Switch.py","frenetic_frenetic_app.py" , "pyretic_pyretic_app.py" , "kinetic_kinetic_app.py" , "floodlight_Hub.java"]
   #testCases = ["test_flow_rules" , "test_pingall"]
   testCases = ["test_flowrules"]
   outputWriters = ["json_writer"]
   networkTopoName = "SimpleTopo"
   #mininetProcess = obj.runMininet(networkTopoName , networkTopoName, portnIP)
   #is_running = False;
   for controllerName in controllers:
        controllerObject = obj.getControllerObject(controllerName)
   	if not isinstance(controllerObject, controller):
                print controllerName +" is not an instance of controller"
                controllers.remove(controllerName)
		continue

   for applicationName in applications:
	l =  applicationName.split("_")
        controllerName = l.pop(0)
        appName = "_".join(l)
        appRunnerObject = obj.getAppRunnerObject(controllerName)
        if not isinstance(appRunnerObject, application_runner):
                print applicationName +" is not an instance of application"
		applications.remove(applicationName)
                continue

   for testCaseName in testCases:
	testCaseObject = obj.getTestCaseObject(testCaseName)
	if not isinstance(testCaseObject, test):
                print testCaseName +" is not an instance of test"
		testCases.remove(testCaseName)
                continue

   if(len(controllers) <= 0 or len(applications) <=0 or len(testCases) <= 0):
	print "There should be atleast one controller, one application and one test case \n"
	print "Exiting......."
	sys.exit(-1)

   for controllerName in controllers:
	portnIP = obj.getIPnPort(controllerName)
	controllerObject = obj.getControllerObject(controllerName)
	controllerObject.runController(portnIP)
	for testCaseName in testCases:
		testCaseObject = obj.getTestCaseObject(testCaseName)
                testCaseObject.execute(config = portnIP )
		for applicationName in applications:
			if applicationName.startswith(controllerName+"_"):
				l = applicationName.split("_")
				l.pop(0)
				applicationName = "_".join(l)
				appRunnerObject = obj.getAppRunnerObject(controllerName)
   				appRunnerObject.runApp(applicationName , portnIP)
				mininetProcess = obj.runMininet(networkTopoName , networkTopoName, portnIP)
				#obj.generateTraffic(mininetProcess)
				appRunnerObject.stopApp()
				obj.stopMininet(mininetProcess)
   		result = testCaseObject.result()
		#print result #time.sleep(5)
		resultDict = {}
   		resultDict["controller"] = controllerName
   		resultDict["testcase"] = testCaseName
   		resultDict["result"] = result
		for writerName in outputWriters:
			writerObject = obj.getOutputWriteObject(writerName)
   			writerObject.write(resultDict)
   	controllerObject.stopController()

   
   '''controllerName = "floodlight"
   controllerDict = {}
   applicationName = "Hub.java"
   appDict = {}
   networkTopoName = "SimpleTopo"
   testCaseName = "test_flowrules"
   duration = 60
   #testCase
   writerName = "json_writer"
   portnIP = obj.getIPnPort(controllerName)
   #print portnIP
   #sys.exit(0)
   #start controller
   controllerObject = obj.getControllerObject(controllerName)
   controllerObject.runController(portnIP["ip"],portnIP["port"])
   #run app
   testCaseObject = obj.getTestCaseObject(testCaseName)
   testCaseObject.execute(duration=duration)
   appRunnerObject = obj.getAppRunnerObject(controllerName)
   appRunnerObject.runApp(applicationName , portnIP)
   mininetProcess = obj.runMininet(networkTopoName , networkTopoName, portnIP)
   #testCaseObject = obj.getTestCaseObject(testCaseName)
   result = testCaseObject.result()
   print result
   resultDict = {}
   resultDict["controller"] = controllerName
   resultDict["testcase"] = testCaseName
   resultDict["result"] = result
   resultsDict[applicationName] = resultDict
   writerObject = obj.getOutputWriteObject(writerName)
   writerObject.write(resultsDict)   
   obj. stopMininet()	
   

   #iet = networkObject.start(portnIP)
   #stop app
   appRunnerObject.stopApp()
   controllerObject.stopController()
   #print resultsDict		
   #print "end Program"
   '''
