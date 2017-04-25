import sys,logging
import frenetic
from frenetic.syntax import *
from frenetic.packet import *
from network_information_base import *

class LearningApp3(frenetic.App):

  client_id = "l2_learning"

  def __init__(self):
    frenetic.App.__init__(self)     
    self.nib = NetworkInformationBase(logging)

  def switch_up(self , switch_id, ports): #def connected(self):
    def handle_current_switches(switches):
      logging.info("Connected to Frenetic - Switches: "+str(switches))
      #P = And[IPProtoEq(6), TCPDstPortEq(80), IP4SrcEq("10.0.0.1"), IP4DstEq("10.0.02")]
      #Filter(P) >> drop
      self.nib.set_ports( ports )
      self.update( id >> SendToController("learning_app") )
    self.current_switches(callback=handle_current_switches)

  def policy_for_dest(self, mac_port):
    (mac, port) = mac_port
    return Filter( EthDstEq(mac) ) >> SetPort(port)
    #return IfThenElse(Filter(EthTypeEq(0x800) & TCPDstPortEq(80) & IP4SrcEq("10.0.0.1") & IP4DstEq("10.0.02")), drop, Filter(EthDstEq(mac)) >> SetPort(port))

  def policies_for_dest(self, all_mac_ports):
    return [ self.policy_for_dest(mp) for mp in all_mac_ports ]

  def policy(self):
    return \
      IfThenElse(
        EthSrcNotEq( self.nib.all_learned_macs() ) | 
          EthDstNotEq( self.nib.all_learned_macs() ),
        SendToController("learning_app"),
        Union( self.policies_for_dest(self.nib.all_mac_port_pairs()) )
      )

  def packet_in(self, dpid, port_id, payload):
    nib = self.nib
    #P = And[ IPProtoEq(6), TCPDstPortEq(80), IP4SrcEq("10.0.0.1"), IP4DstEq("10.0.02") ]
    #Filter(P) >> drop
    
    pkt = Packet.from_payload(dpid, port_id, payload)
    src_mac = pkt.ethSrc
    dst_mac = pkt.ethDst
    #print pkt
    print pkt.ethType
    #if pkt.ethType == 0x800:
	#P = And[ IPProtoEq(6), TCPDstPortEq(80), IP4SrcEq("10.0.0.1"), IP4DstEq("10.0.02") ]
    	#Filter(P) >> drop

    # If we haven't learned the source mac, do so
    #if pkt.ethType != 2054:
    if nib.port_for_mac( src_mac ) == None:
      	nib.learn( src_mac, port_id)
      	self.update(self.policy())
    '''else:
	print "inside firewall block"
	P = And[ IPProtoEq(6), TCPDstPortEq(80), IP4SrcEq("10.0.0.1"), IP4DstEq("10.0.02"), EthTypeEq(0x800) ]
	self.update(Filter(P) >> drop)
	'''
    # Look up the destination mac and output it through the
    # learned port, or flood if we haven't seen it yet.
    dst_port = nib.port_for_mac( dst_mac )
    if  dst_port != None:
      actions = SetPort(dst_port)
    else:
      actions = SetPort( nib.all_ports_except(port_id) )
    self.pkt_out(dpid, payload, actions )

if __name__ == '__main__':
  logging.basicConfig(\
    stream = sys.stderr, \
    format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO \
  )
  app = LearningApp3()
  app.start_event_loop()  

