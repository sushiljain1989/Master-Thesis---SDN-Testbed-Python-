import sys, logging
import frenetic
from frenetic.syntax import *
from frenetic.packet import *
from network_information_base import *

class LearningApp1(frenetic.App):

  client_id = "l2_learning"

  def __init__(self):
    frenetic.App.__init__(self)     
    self.nib = NetworkInformationBase(logging)

  def connected(self):
	logging.info("Connection to controller is established")    
#def handle_current_switches(switches):
     # logging.info("Connected to Frenetic - Switches: "+str(switches))
      #dpid = switches.keys()[0]
      #self.nib.set_ports( switches[dpid] )
      #self.update( id >> SendToController("learning_app") )
    #self.current_switches(callback=handle_current_switches)

  def switch_up(self , switch_id, ports):
	#self.nib.set_ports(ports)
	self.update( id >> SendToController("learning_app") )

  def packet_in(self, dpid, port_id, payload):
    #nib = self.nib
    print "packet received"
    pkt = Packet.from_payload(dpid, port_id, payload)
    actions=""
    if pkt.vlan == 100 or pkt.vlan == 200:
    	a = Filter(VlanEq(200)) >> SetPort([1,3])
    	b = Filter(VlanEq(100)) >> SetPort([2,4])
    	self.update( a | b )
	'''if(port_id%2 == 0):
        	actions = SetPort( [2,4] )
    	else:
        	actions = SetPort( [1,3] )'''

    #self.pkt_out(dpid, payload, actions )
	#src_mac = pkt.ethSrc
    #dst_mac = pkt.ethDst

    # If we haven't learned the source mac, do so
    #if nib.port_for_mac( src_mac ) == None:
     # nib.learn( src_mac, port_id)

    # Look up the destination mac and output it through the
    # learned port, or flood if we haven't seen it yet.
    #dst_port = nib.port_for_mac( dst_mac )
    #if  dst_port != None:
      #actions = SetPort(dst_port)
    #else:
    #if(port_id%2 == 0):
    #	actions = SetPort( [2,4] )
    #else:
	#actions = SetPort( [1,3] )

    #self.pkt_out(dpid, payload, actions )

if __name__ == '__main__':
  logging.basicConfig(\
    stream = sys.stderr, \
    format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO \
  )
  app = LearningApp1()
  app.start_event_loop()  

