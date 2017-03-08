import sys
from test import test
import ConfigParser
import subprocess
import os
import time
import pexpect
import signal
import netifaces
import threading
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
		file_path = TestCase.testBedHomePath+switchI+".log"
		sys.exit(-1)
		if os.path.exists(file_path):
			os.remove(file_path)
                waitTime = 60.0
                spentTime = 0.0
                while True:
                        if switchI in netifaces.interfaces():
                                process = subprocess.Popen(["sudo ovs-ofctl dump-flows "+switchI+" >> "+file_path], shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                                time.sleep(0.1)
                                spentTime+=0.1
                                if waitTime <= spentTime:
                                        break
                        else:
                                time.sleep(0.01)

class TestCase():
    #appsDir = ""
    controllerName = ""
    configFiles = {}
    mainConfigFile = ""
    testBedHomePath = ""
    def readConfigFile(self):

        if TestCase.mainConfigFile == None or TestCase.mainConfigFile == "":
            raise Exception('Please provide absolute path for config.ini')

        else:
            print TestCase.mainConfigFile
	    config = ConfigParser.ConfigParser()
            config.read(TestCase.mainConfigFile)
	    options = config.options(TestCase.controllerName)
            self.dictionary = dict()
            for option in options:
                self.dictionary[option] = config.get(TestCase.controllerName, option)
	    #print self.dictionary
	    sectionName = "misc"
	    options = config.options(sectionName)
	    for option in options:
                self.dictionary[option] = config.get(sectionName, option)
	    return self.dictionary

    #def setAppsDir(self, appsDir=None):
	#pass

    def additionalConfigFile(self, configFilePath=None, configFileName = None ):
        pass

    def startController(self, additionalConfigFiles = None):
        pass

    def startApplication(self, additionalConfigFiles = None):
        pass

    def stopApplication(self, additionalConfigFiles = None):
        pass

    def stopController(self, additionalConfigFiles = None):
        pass

    def setTopology(self, topoFileName, nwTopoName):
	self.topoFileName = topoFileName
	self.nwTopoName = nwTopoName
	

    def runMininet(self, configs):
        #bgThread = threading.Thread(target=runovsOfctlPeriodically, args=("s1",))
        #bgThread.daemon = True
        #bgThread.start()
        # print configs
        # fd = sys.stdin.fileno()
        # fl = fcntl.fcntl(fd , fcntl.F_GETFL)
        # fcntl.fcntl(fd , fcntl.F_SETFL , fl | os.O_NONBLOCK)
        process = subprocess.Popen("sudo mn --custom " + self.topoFileName+" --topo=" + self.nwTopoName + " --controller=remote,ip=" +configs['ip'] + ",port="+configs['port'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        # process.expect(pexpect.EOF)
        # stdout,stderr = process.communicate("pingall")
        # print stdout
        # print "stderrrrrrrrrrr"
        # print stderr
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                output.strip()
                break
        # print process.poll()
        # thread.daemon = True
        # thread.start()
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
        # result = ""
        return process

    def generateTraffic(self, mininetProcess):
	runTime = 5
        startTime = 1
        #print "starting mail traffic"
	'''time.sleep(1)
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
	'''
	startTime = 1
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


    def stopMininet(self, process):
        # os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        # time.sleep(1)
        cmd = 'ps -ef | awk \'/[m]n/{print $2}\''  # 'lsof -t -i:{0}'.format(self.port)
        pid = subprocess.check_output(cmd, shell=True)
        killcmd2 = 'sudo kill -9 {0}'.format(pid.strip().replace('\n', ' '))
        os.system(killcmd2)
        subprocess.Popen("sudo mn -c", shell=True)
        time.sleep(2)

    def setApplicationName(self , applicationName):
        self.applicationName = applicationName

    def setTestBedHome(self, testBedHomePath = '/home/vagrant/python/Master---Thesis/'):
        pass

    def runTestCase(self,applicationName):
	if not hasattr(self, 'topoFileName') or not hasattr(self, 'topoFileName'):
		raise Exception('Please provide both network topology file and topology name')
	if self.nwTopoName == None or self.nwTopoName == "" or self.topoFileName == None or self.topoFileName == "" :
		raise Exception('Please provide both network topology file and topology name')
        self.startController()
        self.startApplication(applicationName)
        mnProcess = self.runMininet(self.dictionary)
        self.stopApplication()
        self.stopMininet(mnProcess)
        self.stopController()
