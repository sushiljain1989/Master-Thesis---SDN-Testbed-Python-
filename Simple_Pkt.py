import sys
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

    print "Packets dropped during pingall : " + str( net.pingAll() ) + "%"
    h1, h2, s1 = net.get('h1', 'h2', 's1')
    #print "iperf between h1 and h2"
    #net.iperf((h1, h2))
    #h1.cmdPrint('iperf -s &')
    #h2.cmdPrint('iperf -t 10 -c', h1.IP() )
    flowRules =  s1.dpctl('dump-flows')
    print "# of installed flow rules: " + str( len(flowRules.split('\r')) - 2 ) #print isinstance(flowRules, list)
    #print isinstance(flowRules, str)
    print "Stopping Mininet"
    net.stop()

if __name__ == '__main__':
   cmdargs = str(sys.argv)
   ip = str(sys.argv[1])
   port = str(sys.argv[2])
   setLogLevel('info')
   run(ip , port)
~                          