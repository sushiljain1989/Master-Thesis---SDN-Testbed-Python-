import sys
import time
import subprocess
from Test import Test
class TestFlowrules(Test):
	
	def __init__(self, testbedpath, config):
		self.testbedname = testbedpath
		#print config
		#self.config = config	

	def result(self):
		count = 0
		while True:
			if self.process.poll() == None:
				#print "waiting"
				time.sleep(1)
			else: 
				break
		f = open(self.testbedname+"my.log" , "r")
		#print "file opened"
                for line in f.readlines():
			#print "Line : "+line
                	if "New flow (0)" in line:
				count+=1
			
		f.close()
		#print "file closed"
		result = {"flow rules" : count}
		return result
		

	def execute(self, proces = None, config = None):
		#stdout,stderr = process.communicate("pingall")
		#print stderr
		#self.testbedname = testbedname
		#print self.config
		self.process = subprocess.Popen(["sudo timeout 60 tshark -i lo -d tcp.port=="+self.config['port']+",openflow -V > "+self.testbedname+"my.log"],shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
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
