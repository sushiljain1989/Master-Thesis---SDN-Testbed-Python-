import sys
import time
class test_flow_rules:
#test_flow_rules.py
	def execute(self , process):
		#stdout,stderr = process.communicate("pingall")
		#print stderr
		process.stdin.write("dpctl dump-flows \n")
		process.stdin.flush()
		time.sleep(2)
		result = ""
		while True:
                        #print "before readline"
			output = process.stdout.readline()
			#print "after readline"
			#print process.poll()
                        if output == '' and process.poll() is not None:
                                break
                        if output:
                                line =  output.strip()
				print line
				#if line.startswith('***') or line.startswith('NXST_FLOW'):
					#continue
		return "test"
		#process.expect(".*")
		#print process.before
		#print process.after
		#return "Result from demo test case"
