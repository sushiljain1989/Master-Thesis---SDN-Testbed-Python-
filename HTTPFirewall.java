/**
*    Copyright 2011, Big Switch Networks, Inc. 
*    Originally created by David Erickson, Stanford University
* 
*    Licensed under the Apache License, Version 2.0 (the "License"); you may
*    not use this file except in compliance with the License. You may obtain
*    a copy of the License at
*
*         http://www.apache.org/licenses/LICENSE-2.0
*
*    Unless required by applicable law or agreed to in writing, software
*    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
*    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
*    License for the specific language governing permissions and limitations
*    under the License.
**/

package net.floodlightcontroller.httpfirewall;
import net.floodlightcontroller.packet.*;
import net.floodlightcontroller.packet.Ethernet;
import org.projectfloodlight.openflow.protocol.match.Match;
import net.floodlightcontroller.util.OFMessageUtils;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import net.floodlightcontroller.core.FloodlightContext;
import net.floodlightcontroller.core.IFloodlightProviderService;
import net.floodlightcontroller.core.IOFMessageListener;
import net.floodlightcontroller.core.IOFSwitch;
import net.floodlightcontroller.core.module.FloodlightModuleContext;
import net.floodlightcontroller.core.module.FloodlightModuleException;
import net.floodlightcontroller.core.module.IFloodlightModule;
import net.floodlightcontroller.core.module.IFloodlightService;

import org.projectfloodlight.openflow.protocol.*;
import org.projectfloodlight.openflow.protocol.OFMessage;
import org.projectfloodlight.openflow.protocol.OFPacketIn;
import org.projectfloodlight.openflow.protocol.OFPacketOut;
import org.projectfloodlight.openflow.protocol.OFType;
import org.projectfloodlight.openflow.protocol.OFVersion;
import org.projectfloodlight.openflow.protocol.action.OFAction;
import org.projectfloodlight.openflow.protocol.action.OFActionOutput;
import org.projectfloodlight.openflow.protocol.match.MatchField;
import org.projectfloodlight.openflow.types.*;
import org.projectfloodlight.openflow.types.OFPort;

/**
 *
 * @author David Erickson (daviderickson@cs.stanford.edu) - 04/04/10
 */
public class HTTPFirewall implements IFloodlightModule, IOFMessageListener {
	//private enum HubType {USE_PACKET_OUT, USE_FLOW_MOD};
	private HashMap<MacAddress , OFPort> hello = null;

    private IFloodlightProviderService floodlightProvider;

    /**
     * @param floodlightProvider the floodlightProvider to set
     */
    public void setFloodlightProvider(IFloodlightProviderService floodlightProvider) {
        this.floodlightProvider = floodlightProvider;
    }

    @Override
    public String getName() {
        return HTTPFirewall.class.getPackage().getName();
    }

    public Command receive(IOFSwitch sw, OFMessage msg, FloodlightContext cntx) {
    	OFPacketIn pi = (OFPacketIn)msg;
    	OFFlowAdd.Builder fmb = sw.getOFFactory().buildFlowAdd();
        Match myMatch = sw.getOFFactory().buildMatch().
        				setExact(MatchField.ETH_TYPE, EthType.IPv4).
        				setExact(MatchField.IP_PROTO, IpProtocol.TCP).
                        setExact(MatchField.IPV4_DST, IPv4Address.of(IPv4.toIPv4Address("10.0.0.2"))).
                        setExact(MatchField.IPV4_SRC, IPv4Address.of(IPv4.toIPv4Address("10.0.0.1"))).
			setExact(MatchField.TCP_DST, TransportPort.of(80)).
                        build();
        
        fmb = sw.getOFFactory().buildFlowAdd();
        
        fmb.setMatch(myMatch);
        
        //fmb.setBufferId(pi.getBufferId())
        //.setXid(pi.getXid());
        fmb.setPriority(10);
        
        OFMessage dropMessage = fmb.build();
        sw.write(dropMessage);
    	System.out.println(dropMessage);
	System.out.println("Firewall end");
    	
    	OFMessage outMessage;
    	Ethernet eth = IFloodlightProviderService.bcStore.get(cntx, IFloodlightProviderService.CONTEXT_PI_PAYLOAD);
        MacAddress srcMac = eth.getSourceMACAddress();
        MacAddress dstMac = eth.getDestinationMACAddress();
       
        if(hello == null)
        	hello = new HashMap<MacAddress, OFPort>();
        
        
        OFPort inPort = OFMessageUtils.getInPort(pi);
        inPort.getPortNumber();
        
        if(!hello.containsKey(srcMac))
        {
        	hello.put(srcMac, inPort);
        }
        
        OFPort outport = null;
        
        if(hello.containsKey(dstMac))
        {
        	outport = hello.get(dstMac);
        }
        
        if(outport != null)
        {
	//System.out.println("Inside Mac Learning");

         fmb = sw.getOFFactory().buildFlowAdd();
         myMatch = sw.getOFFactory().buildMatch().setExact(MatchField.ETH_DST, dstMac).build();
        
        fmb.setMatch(myMatch);
        fmb.setBufferId(pi.getBufferId())
        .setXid(pi.getXid());

        // set actions
        OFActionOutput.Builder actionBuilder = sw.getOFFactory().actions().buildOutput();
        actionBuilder.setPort(outport);
        fmb.setPriority(2);
        fmb.setActions(Collections.singletonList((OFAction) actionBuilder.build()));
        outMessage = fmb.build();
        
        
	//System.out.println(outMessage);
        
  
        }
        else
        {

	//System.out.println("Flooding \n");
        	OFPacketOut.Builder pob = sw.getOFFactory().buildPacketOut();
            pob.setBufferId(pi.getBufferId()).setXid(pi.getXid()).setInPort((pi.getVersion().compareTo(OFVersion.OF_12) < 0 ? pi.getInPort() : pi.getMatch().get(MatchField.IN_PORT)));
            
            // set actions
            OFActionOutput.Builder actionBuilder = sw.getOFFactory().actions().buildOutput();
            actionBuilder.setPort(OFPort.FLOOD);
            pob.setActions(Collections.singletonList((OFAction) actionBuilder.build()));

            // set data if it is included in the packetin
            if (pi.getBufferId() == OFBufferId.NO_BUFFER) {
                byte[] packetData = pi.getData();
                pob.setData(packetData);
            }
            outMessage = pob.build();
        }
        
        sw.write(outMessage);
        
		
        
        return Command.CONTINUE;
	
	}
    /*
    private OFMessage createHubFlowMod(IOFSwitch sw, OFMessage msg) {
    	OFPacketIn pi = (OFPacketIn) msg;
        OFFlowAdd.Builder fmb = sw.getOFFactory().buildFlowAdd();
        fmb.setBufferId(pi.getBufferId())
        .setXid(pi.getXid());

        // set actions
        OFActionOutput.Builder actionBuilder = sw.getOFFactory().actions().buildOutput();
        actionBuilder.setPort(OFPort.FLOOD);
        fmb.setActions(Collections.singletonList((OFAction) actionBuilder.build()));

        return fmb.build();
    }
    
    private OFMessage createHubPacketOut(IOFSwitch sw, OFMessage msg) {
    	OFPacketIn pi = (OFPacketIn) msg;
        OFPacketOut.Builder pob = sw.getOFFactory().buildPacketOut();
        pob.setBufferId(pi.getBufferId()).setXid(pi.getXid()).setInPort((pi.getVersion().compareTo(OFVersion.OF_12) < 0 ? pi.getInPort() : pi.getMatch().get(MatchField.IN_PORT)));
        
        // set actions
        OFActionOutput.Builder actionBuilder = sw.getOFFactory().actions().buildOutput();
        actionBuilder.setPort(OFPort.FLOOD);
        pob.setActions(Collections.singletonList((OFAction) actionBuilder.build()));

        // set data if it is included in the packetin
        if (pi.getBufferId() == OFBufferId.NO_BUFFER) {
            byte[] packetData = pi.getData();
            pob.setData(packetData);
        }
        return pob.build();  
    }
*/
    @Override
    public boolean isCallbackOrderingPrereq(OFType type, String name) {
        return false;
    }

    @Override
    public boolean isCallbackOrderingPostreq(OFType type, String name) {
        return false;
    }

    // IFloodlightModule
    
    @Override
    public Collection<Class<? extends IFloodlightService>> getModuleServices() {
        // We don't provide any services, return null
        return null;
    }

    @Override
    public Map<Class<? extends IFloodlightService>, IFloodlightService>
            getServiceImpls() {
        // We don't provide any services, return null
        return null;
    }

    @Override
    public Collection<Class<? extends IFloodlightService>>
            getModuleDependencies() {
        Collection<Class<? extends IFloodlightService>> l = 
                new ArrayList<Class<? extends IFloodlightService>>();
        l.add(IFloodlightProviderService.class);
        return l;
    }

    @Override
    public void init(FloodlightModuleContext context)
            throws FloodlightModuleException {
        floodlightProvider = context.getServiceImpl(IFloodlightProviderService.class);
    }

    @Override
    public void startUp(FloodlightModuleContext context) {
        floodlightProvider.addOFMessageListener(OFType.PACKET_IN, this);
    }
}
