import sys
import mysql.connector
from mysql.connector import Error
from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI

class SimpleTopo25(Topo):

    def __init__(self):

        Topo.__init__(self)

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
	h4 = self.addHost('h4')
	h5 = self.addHost('h5')
	h6 = self.addHost('h6')
	h7 = self.addHost('h7')
	h8 = self.addHost('h8')
	h9 = self.addHost('h9')
	h10 = self.addHost('h10')
        s1 = self.addSwitch('s1')
        
	s2 = self.addSwitch('s2')
        self.addLink(h1, s2)
	self.addLink(h2, s2)
	self.addLink(h3, s2)
	self.addLink(h4, s2)
	self.addLink(h5, s2)
	
	s3 = self.addSwitch('s3')
	self.addLink(h6, s3)
	self.addLink(h7, s3)
	self.addLink(h8, s3)
	self.addLink(h9, s3)
	self.addLink(h10, s3)

	#s4 = self.addSwitch('s4')
        #self.addLink(h5, s4)
        #self.addLink(h6, s4)
	
	self.addLink(s1 , s2)
	self.addLink(s1 , s3)
	#self.addLink(s1 , s4)        

	#sw2 = self.addSwitch('s2')
        #self.addLink(h1, s1)
        #self.addLink(h2, s1)
	#self.addLink(h4 , sw2)
	#self.addLink(h5 , sw2)
	#self.addLink(s1 , sw2)

    #def start(self , configs):
    #print("%s" % ip)
    #print ("%s" % port)
    #c = RemoteController('c', ip='127.0.0.1', port='6633')
    	#net = Mininet(topo=SimpleTopo(), host=CPULimitedHost, controller=None)
    	#net.addController('c', controller=RemoteController, ip="127.0.0.1", port=6633 )
    	#net.start()

    #pingall =  str( net.pingAll() )
    #print pingall
    #updateJobResult(pingall , "pingall")
    #h1, h2, s1 = net.get('h1', 'h2', 's1')
    #print "iperf between h1 and h2"
    #net.iperf((h1, h2))
    #h1.cmdPrint('iperf -s &')
    #h2.cmdPrint('iperf -t 10 -c', h1.IP() )
    #flowRules =  s1.dpctl('dump-flows')
    #flowRulesS =  str( len(flowRules.split('\r')) - 2 ) #print isinstance(flowRules, list)
    #print isinstance(flowRules, str)
    #print flowRulesS
    #updateJobResult(flowRulesS , "flow_rules")
    #print "Stopping Mininet"
    	#return self.net

    #def stop(self):
    #	self.net.stop()

#def updateJobResult(self, result , testcase):
#	try:
#		conn = mysql.connector.connect(host='localhost', database='python_mysql', user='root', password='secret')
#		status = "Processing"
#		data = (result , status)
#		if conn.is_connected():
#			cursor = conn.cursor
#			if testcase == "pingall":
#				query = """ update jobs set pingall = %s where status = %s """
#			if testcase == "flow_rules":
#				query =  """ update jobs set flow_rules  = %s where status = %s """	
#			cursor.execute(query , data)
#			conn.commit()
#			cursor.close()
#			conn.close()
#	except Error as e:
#		print(e)
#	finally:
#		testcase = testcase


#if __name__ == '__main__':
#   cmdargs = str(sys.argv)
#   ip = str(sys.argv[1])
#   port = str(sys.argv[2])
#   setLogLevel('info')
#   run(ip , port)
topos = {'SimpleTopo25': ( lambda: SimpleTopo25() ) }
