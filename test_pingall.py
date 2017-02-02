import sys
import time
class test_pingall:

	def execute(self , process):
		#stdout,stderr = process.communicate("pingall")
		#print stderr
		process.stdin.write("pingall \n")
		process.stdin.flush()
		time.sleep(0.5)
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
				if line.startswith('*** Results: '):
					result = line
					break
		return result
		#process.expect(".*")
		#print process.before
		#print process.after
		#return "Result from demo test case"
