import sys
import mysql.connector
from mysql.connector import Error
from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI

class SimplePktSwitch(Topo):

    def __init__(self, **opts):

        super(SimplePktSwitch, self).__init__(**opts)

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        s1 = self.addSwitch('s1', dpid="0000000000000001")

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)



def run(cip , cport):
    #print("%s" % ip)
    #print ("%s" % port)
    #c = RemoteController('c', ip='127.0.0.1', port='6633')
    net = Mininet(topo=SimplePktSwitch(), host=CPULimitedHost, controller=None)
    net.addController('c', controller=RemoteController, ip=cip, port=int(cport) )
    net.start()

    pingall =  str( net.pingAll() )
    print pingall
    #updateJobResult(pingall , "pingall")
    h1, h2, s1 = net.get('h1', 'h2', 's1')
    #print "iperf between h1 and h2"
    #net.iperf((h1, h2))
    #h1.cmdPrint('iperf -s &')
    #h2.cmdPrint('iperf -t 10 -c', h1.IP() )
    flowRules =  s1.dpctl('dump-flows')
    flowRulesS =  str( len(flowRules.split('\r')) - 2 ) #print isinstance(flowRules, list)
    #print isinstance(flowRules, str)
    print flowRulesS
    #updateJobResult(flowRulesS , "flow_rules")
    #print "Stopping Mininet"
    net.stop()

def updateJobResult(result , testcase):
	try:
		conn = mysql.connector.connect(host='localhost', database='python_mysql', user='root', password='secret')
		status = "Processing"
		data = (result , status)
		if conn.is_connected():
			cursor = conn.cursor
			if testcase == "pingall":
				query = """ update jobs set pingall = %s where status = %s """
			if testcase == "flow_rules":
				query =  """ update jobs set flow_rules  = %s where status = %s """	
			cursor.execute(query , data)
			conn.commit()
			cursor.close()
			conn.close()
	except Error as e:
		print(e)
	finally:
		testcase = testcase


if __name__ == '__main__':
   cmdargs = str(sys.argv)
   ip = str(sys.argv[1])
   port = str(sys.argv[2])
   setLogLevel('info')
   run(ip , port)
