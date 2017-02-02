import sys
import time
import subprocess
class test_flowrules:
	
	def result(self):
		count = 0
		while True:
			if self.process.poll() == None:
				#print "waiting"
				time.sleep(1)
			else: 
				break
		f = open("/home/vagrant/python/Master---Thesis/my.log" , "r")
		#print "file opened"
                for line in f.readlines():
			#print "Line : "+line
                	if "New flow (0)" in line:
				count+=1
			
		f.close()
		#print "file closed"
		return count
		

	def execute(self , proces = None, config = None):
		#stdout,stderr = process.communicate("pingall")
		#print stderr
		self.process = subprocess.Popen(["sudo timeout "+str(config['duration'])+" tshark -i lo -d tcp.port=="+config['port']+",openflow -V > /home/vagrant/python/Master---Thesis/my.log"],shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
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
