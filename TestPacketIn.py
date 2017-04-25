import sys
import time
import subprocess
import collections
from Test import Test
class TestPacketIn(Test):

	def __init__(self, testbedpath, config):
                self.testbedname = testbedpath
                self.config = config

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
		incoming_pkts = 0
		outgoing_pkts = 0
		pkt_events = {}
		epochTime = 0.0
		prevepochtime = 0.0
		diff = 0.2
		incoming_packets = {}
                for line in f.readlines():
			#print "Line : "+line
			if line.strip().startswith("Epoch Time"):
				if prevepochtime == 0.0:
					prevepochtime = float(line.split()[2])
				epochTime = float(line.split()[2])
				if epochTime-prevepochtime >= diff:
					incoming_packets[epochTime] = {"Packets": incoming_pkts, "duration": epochTime-prevepochtime}
					prevepochtime = epochTime
					epochTime = 0.0
					#incoming_packets[prevepochtime] = {"Packets": incoming_pkts, "duration": }
					incoming_pkts = 0
				
                	elif "OFPT_PACKET_IN" in line:
					incoming_pkts+=1
				
			'''elif "OFPT_PACKET_OUT" in line:
				pkt_events[epochTime] = "PACKET_OUT"
			elif "Delete all matching flows" in line:
				pkt_events[epochTime] = "FLOW_MOD_DELETE"
			elif "New flow (0)" in line:
				pkt_events[epochTime] = "FLOW_MOD_ADD_NEW"'''
			
		f.close()
		#packets = { "Incoming Packets(PKT_IN)" : incoming_pkts , "Outgoing Packets(PKT_OUT)" : outgoing_pkts }
		#print "file closed"
		result = {}
		result["Packets_at_controller"] = collections.OrderedDict(sorted(incoming_packets.items(), key=lambda t: t[0])) #sorted(incoming_packets)
		return result
		

	def execute(self, proces = None, config = None):
		#stdout,stderr = process.communicate("pingall")
		#print stderr
		#self.testbedname = testbedname
		self.process = subprocess.Popen(["sudo timeout "+str(self.config['duration'])+" tshark -i lo -d tcp.port=="+self.config['port']+",openflow -V > "+self.testbedname+"my.log"],shell=True,stdin=subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
                output = self.process.stdout.readline()
		while True: 
                	if output == '' and self.process.poll() is not None:
                                break
                        if output:
                                output.strip()
				break 
