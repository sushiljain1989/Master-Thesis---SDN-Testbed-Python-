import sys
import time
import subprocess
class test_packets_event:
	
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
		incoming_pkts = 0
		outgoing_pkts = 0
		pkt_events = {}
		epochTime = 0.0
                for line in f.readlines():
			#print "Line : "+line
			if line.strip().startswith("Epoch Time"):
				epochTime = line.split()[2]
                	elif "OFPT_PACKET_IN" in line:
				pkt_events[epochTime] = "PACKET_IN"
				epochTime = 0.0	
			elif "OFPT_PACKET_OUT" in line:
				pkt_events[epochTime] = "PACKET_OUT"
			elif "Delete all matching flows" in line:
				pkt_events[epochTime] = "FLOW_MOD_DELETE"
			elif "New flow (0)" in line:
				pkt_events[epochTime] = "FLOW_MOD_ADD_NEW"
			
		f.close()
		#packets = { "Incoming Packets(PKT_IN)" : incoming_pkts , "Outgoing Packets(PKT_OUT)" : outgoing_pkts }
		#print "file closed"
		timestamps = sorted(pkt_events)
		prev_event = ""
		startTime = 0.0
		latestTime = 0.0
		pkts = 1
		events_dict = {}
		for key in timestamps:
			if prev_event == "":
				prev_event = pkt_events[key]
				startTime = float(key)
				latestTime = float(key)
			
			elif prev_event == pkt_events[key]:
				latestTime = float(key)
				pkts+=1
			
			elif prev_event != pkt_events[key]:
				events_dict[startTime] = { "event":prev_event , "start":startTime , "end":latestTime , "duration":latestTime-startTime , "numPkts":pkts }
				startTime = float(key)
				latestTime = float(key)
				prev_event = pkt_events[key]
				pkts = 1
			
		
		return events_dict
		

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
