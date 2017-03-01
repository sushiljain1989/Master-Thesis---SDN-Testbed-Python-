import sys
import time
import subprocess
from test import test
class test_periodic_flowrules(test):
	
	def result(self):
		switchI = "s1"
		'''count = 0
		frames = []
		frame = ""
		start = 0
		epoch = []
		while True:
			if self.process.poll() == None:
				#print "waiting"
				time.sleep(1)
			else: 
				break
		'''
		f = open(self.testbedname+switchI+".log" , "r")
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
		#print "file closed"
		print len(rulesList)
		return rulesList
		

	def execute(self, testbedname, proces = None, config = None):
		#stdout,stderr = process.communicate("pingall")
		#print stderr
		self.testbedname = testbedname
		self.process = subprocess.Popen(["sudo timeout "+str(config['duration'])+" tshark -i lo -d tcp.port=="+config['port']+",openflow -V > "+self.testbedname+"my.log"],shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                #process.expect(pexpect.EOF)
                #stdout,stderr = process.communicate("pingall")
                #print stdout
                #print "stderrrrrrrrrrr"
                #print stderr
		#secs = 0
                #while secs < 10:
                output = self.process.stdout.readline()
		while True: 
                	if output == '' and self.process.poll() is not None:
                                break
                        if output:
                                output.strip()
				break 
		#process.stdin.write("dpctl dump-flows \n")
		#process.stdin.flush()
		#time.sleep(2)
		#result = ""
		#while True:
                        #print "before readline"
			#output = process.stdout.readline()
			#print "after readline"
			#print process.poll()
                        #if output == '' and process.poll() is not None:
                         #       break
                        #if output:
                         #       line =  output.strip()
			#	print line
				#if line.startswith('***') or line.startswith('NXST_FLOW'):
					#continue
		#return "test"
		#process.expect(".*")
		#print process.before
		#print process.after
		#return "Result from demo test case"
