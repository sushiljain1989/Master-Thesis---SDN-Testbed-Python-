import sys, logging
import frenetic
from frenetic.syntax import *
from frenetic.packet import *
from network_information_base import *

class LearningApp1(frenetic.App):

  client_id = "l2_learning"

  def __init__(self):
    frenetic.App.__init__(self)     
    #self.nib = NetworkInformationBase(logging)

  def connected(self):
	logging.info("Connection to controller is established")
	self.mac_port_dict = {}
	#self.mac_switch = {}    
#def handle_current_switches(switches):
     # logging.info("Connected to Frenetic - Switches: "+str(switches))
      #dpid = switches.keys()[0]
      #self.nib.set_ports( switches[dpid] )
      #self.update( id >> SendToController("learning_app") )
    #self.current_switches(callback=handle_current_switches)

  def switch_up(self , switch_id, ports):
	print "ports :"+str(switch_id)
	print ports
	self.update( id >> SendToController("l2_learning") )
  
  def getports(self, in_port_id):
	return [p for p in self.ports if p != in_port_id]

  def packet_in(self, dpid, port_id, payload):
    pkt = Packet.from_payload(dpid, port_id, payload)

    #print port_id
    #print pkt
    #src_mac = pkt.ethSrc
    #dst_mac = pkt.ethDst

    '''if src_mac not in self.mac_port_dict:
	print self.mac_port_dict
	self.mac_port_dict[src_mac] = port_id
	rule = Filter(EthDstEq(src_mac)) >> SetPort(port_id)
	self.update( rule)
	outports = self.getports(port_id)
	self.pkt_out(dpid, payload, SetPort(outports))
    '''




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
    #actions = SetPort( nib.all_ports_except(port_id) )
    #self.pkt_out(dpid, payload, actions )

if __name__ == '__main__':
  #logging.basicConfig(\
   # stream = sys.stderr, \
    #format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO \
  #)
  app = LearningApp1()
  app.start_event_loop()  

