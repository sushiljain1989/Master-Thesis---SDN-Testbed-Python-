import sys,logging
import frenetic
from frenetic.syntax import *
from frenetic.packet import *

class LearningApp3(frenetic.App):

  client_id = "l2_learning"
  ports = {}
  hosts = {}

  def __init__(self):
    frenetic.App.__init__(self)     
    
  def connected(self):
    print "connected"

  def switch_up(self , switch_id, ports):
    self.set_all_ports(switch_id, ports)
    self.update( id >> SendToController("learning_app") )

  def set_all_ports(self, switch_id, ports):
    self.ports[switch_id] = ports

  def port_for_mac_on_switch(self, mac, dpid):
    return self.hosts[mac][1] \
      if mac in self.hosts and self.hosts[mac][0] == dpid else None  

  def is_internal_port(self, dpid, port_id):
    return port_id == 3

  def all_learned_macs_on_switch(self, dpid):
    return [
      mac for mac in self.hosts.keys() if self.hosts[mac][0] == dpid
    ]  

  def all_learned_macs(self):
    return [ mac for mac in self.hosts.keys() ]
  
  def learn(self, mac, dpid, port_id):
    # Do not learn a mac twice
    if mac in self.hosts:
      return

    cd = (dpid, port_id)
    self.hosts[mac] = cd
    print "Learning: "+mac+" attached to "+str(cd)  

  def all_ports_except(self, dpid, in_port_id):
    return [p for p in self.ports[dpid] if p != in_port_id]

  def all_mac_port_pairs_on_switch(self, dpid):
    return [
      (mac, self.hosts[mac][1])
      for mac in self.hosts.keys() if self.hosts[mac][0] == dpid
    ]   
    
  def policy(self):
    #return self.policy_for_edge_switches()
    #self.additional()
    return IfThenElse((IPProtoEq(6) & IP4SrcEq("10.0.0.1") & IP4DstEq("10.0.0.3") & TCPDstPortEq(80) & EthTypeEq(0x800)),drop,self.additional() | self.policy_for_edge_switches())

  def return_other_switch_mac(self, dpid):
	return [
      mac for mac in self.hosts.keys() if self.hosts[mac][0] != dpid
    ]

  def additional(self):
	#[self.poli(dpid) for dpid in self.ports]
	return Union(self.poli(dpid) for dpid in self.ports)

  def poli(self, dpid):
	l  = []
	for mac_1 in self.all_learned_macs_on_switch(dpid):
		for mac_2 in self.return_other_switch_mac(dpid):
			l.append(  Filter(EthDstEq(mac_2) & EthSrcEq(mac_1) ) >> SetPort(3))
	return Union(l)
	#return Filter(dpid) >> IfThenElse(EthDstNotEq(self.all_learned_macs_on_switch(dpid)) & EthDstEq(self.all_learned_macs()), SetPort(3), SendToController("multiswitch"))

  def policy_for_internal(self, dpid):
	return Filter(SwitchEq(dpid)) >> EthDstEq(self.return_other_switch_mac(dpid)) >> Union(self.pols_for_dest(dpid))

  def pols_for_dest(self, dpid):
	return [ self.pol_for_dest(mac) for mac in self.return_other_switch_mac(dpid) ]

  def pol_for_dest(self,mac):
	return Filter(EthDstEq(mac)) >> SetPort(3)
  
  def policy_for_edge_switches(self):
      return Union(
      self.policy_for_edge_switch(dpid)
      for dpid in self.ports
    )

  def policy_for_edge_switch(self, dpid):
    #nib = self.nib
    print self.all_learned_macs()
    """return Filter(SwitchEq(dpid)) >> \
	   IfThenElse(
		EthDstEq( self.all_learned_macs_on_switch(dpid) ),
          	Union( self.policies_for_dest(dpid, self.all_mac_port_pairs_on_switch(dpid)) ),
		IfThenElse(EthDstEq( self.all_learned_macs()), Union( self.pols_for_dest(dpid) ), self.policy_flood(dpid))
		)
    """
    return \
      Filter(SwitchEq(dpid)) >> \
      IfThenElse(
        EthSrcNotEq( self.all_learned_macs_on_switch(dpid) ) &
          PortNotEq(3),
        SendToController("multiswitch"),
        IfThenElse(
          EthDstEq( self.all_learned_macs_on_switch(dpid) ),
          Union( self.policies_for_dest(dpid, self.all_mac_port_pairs_on_switch(dpid)) ),
          self.policy_flood(dpid)
        )
      )
  def policy_flood(self, dpid):
    return Union(
      self.policy_flood_one_port(dpid, p)
      for p in self.ports[dpid]
    )

  def policy_flood_one_port(self, dpid, port_id):
    outputs = SetPort( self.all_ports_except(dpid, port_id) )
    return Filter(PortEq(port_id)) >> outputs      


  def policy_for_dest(self, dpid, mac_port):
    (mac, port) = mac_port
    return Filter(EthDstEq(mac)) >> SetPort(port)

  def policies_for_dest(self, dpid, all_mac_ports):
    return [ self.policy_for_dest(dpid, mp) for mp in all_mac_ports ]        

  def packet_in(self, dpid, port_id, payload):
    
    pkt = Packet.from_payload(dpid, port_id, payload)
    src_mac = pkt.ethSrc
    dst_mac = pkt.ethDst

    # If we haven't learned the source mac, do so
    if self.port_for_mac_on_switch( src_mac, dpid ) == None:
      # Don't learn the mac for packets coming in from internal ports
      if self.is_internal_port(dpid, port_id):
        pass
      else:
        self.learn( src_mac, dpid, port_id )
        self.update(self.policy())

    # Look up the destination mac and output it through the
    # learned port, or flood if we haven't seen it yet.
    dst_port = self.port_for_mac_on_switch( dst_mac, dpid )
    if  dst_port != None:
      actions = SetPort(dst_port)
    else:
      actions = SetPort( self.all_ports_except(dpid, port_id) )
    self.pkt_out(dpid, payload, actions )

if __name__ == '__main__':
  logging.basicConfig(\
    stream = sys.stderr, \
    format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO \
  )
  app = LearningApp3()
  app.start_event_loop()
