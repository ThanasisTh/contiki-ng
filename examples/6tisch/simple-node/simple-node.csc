<?xml version="1.0" encoding="UTF-8"?>
<simconf>
  <project EXPORT="discard">[APPS_DIR]/mrm</project>
  <project EXPORT="discard">[APPS_DIR]/mspsim</project>
  <project EXPORT="discard">[APPS_DIR]/avrora</project>
  <project EXPORT="discard">[APPS_DIR]/serial_socket</project>
  <project EXPORT="discard">[APPS_DIR]/powertracker</project>
  <simulation>
    <title>6-star-mobile-tsch</title>
    <randomseed>123456</randomseed>
    <motedelay_us>1000000</motedelay_us>
    <radiomedium>
      org.contikios.cooja.radiomediums.UDGM
      <transmitting_range>50.0</transmitting_range>
      <interference_range>100.0</interference_range>
      <success_ratio_tx>1.0</success_ratio_tx>
      <success_ratio_rx>1.0</success_ratio_rx>
    </radiomedium>
    <events>
      <logoutput>40000</logoutput>
    </events>
    <motetype>
      org.contikios.cooja.mspmote.Z1MoteType
      <identifier>z11</identifier>
      <description>Z1 Mote Type #z11</description>
      <source EXPORT="discard">[CONFIG_DIR]/node.c</source>
      <commands EXPORT="discard">make clean node.z1 TARGET=z1</commands>
      <firmware EXPORT="copy">[CONFIG_DIR]/node.z1</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.RimeAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Mote2MoteRelations</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.MoteAttributes</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspClock</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspButton</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.Msp802154Radio</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDefaultSerial</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspLED</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDebugOutput</moteinterface>
    </motetype>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>0.0</x>
        <y>0.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>1</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>27.5</x>
        <y>35.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>2</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>-27.5</x>
        <y>35.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>3</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>-45.0</x>
        <y>-15.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>4</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>45.0</x>
        <y>-15.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>5</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>0.0</x>
        <y>-45.0</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>6</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
  </simulation>
  <plugin>
    org.contikios.cooja.plugins.SimControl
    <width>398</width>
    <z>0</z>
    <height>176</height>
    <location_x>2</location_x>
    <location_y>400</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Visualizer
    <plugin_config>
      <moterelations>true</moterelations>
      <skin>org.contikios.cooja.plugins.skins.IDVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.GridVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.TrafficVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.UDGMVisualizerSkin</skin>
      <viewport>1.3291403969762747 0.0 0.0 1.3291403969762747 96.50618443280501 158.53564990427267</viewport>
    </plugin_config>
    <width>400</width>
    <z>3</z>
    <height>400</height>
    <location_x>1</location_x>
    <location_y>1</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.LogListener
    <plugin_config>
      <filter />
      <formatted_time />
      <coloring />
    </plugin_config>
    <width>1080</width>
    <z>2</z>
    <height>1001</height>
    <location_x>400</location_x>
    <location_y>0</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.ScriptRunner
    <plugin_config>
      <script>TIMEOUT(680000, log.log("last msg: " + msg + "\n")); /* milliseconds. print last msg at timeout */

var mobile_node_participation = 30000000;
var mobile_node_rejoin = 80000000;

var association_time = [];
var disassociation_time = [];
var connection_status = [];

motes = sim.getMotes();

for(var i=1; i &lt; motes.length; i++) {
    association_time.push(-1);
    disassociation_time.push(-1);
    connection_status.push(-1);
}

while(1) {
    m = motes[id-1];
    
    if(msg.contains("association done")) {
        association_time[id-2] = time;
        connection_status[id-2] = 1;
//         log.log("ID: " + id + ": Association done at: " + time + "\n");
    }
    if(association_time[id-2] &gt; -1 &amp;&amp; (time - association_time[id-2] &gt; mobile_node_participation)) {
	    var x = m.getInterfaces().getPosition().getXCoordinate();
        var y = m.getInterfaces().getPosition().getYCoordinate();
        m.getInterfaces().getPosition().setCoordinates(x+150, y, 0);
        association_time[id-2] = -1;
    }
    if(msg.contains("leaving the network, stats")) {
        disassociation_time[id-2] = time;
        connection_status[id-2] = -1;
//         log.log("ID: " + id + ": Left the Network at: " + time + "\n");
    }
    if(disassociation_time[id-2] &gt; -1 &amp;&amp; (time - disassociation_time[id-2] &gt; mobile_node_rejoin)) {
	    var x = m.getInterfaces().getPosition().getXCoordinate();
        var y = m.getInterfaces().getPosition().getYCoordinate();
        m.getInterfaces().getPosition().setCoordinates(x-150, y, 0);
        disassociation_time[id-2] = -1;
    }
    if(msg.contains("bc-1") &amp;&amp; id == 1) {
//         log.log("----------------------------------------------------\n");
        var true_channel = motes[0].getInterfaces().getRadio().getChannel();
//         log.log("true_channel: " + true_channel + "\n");
        for(var i=1; i&lt;motes.length; i++) {
            if(connection_status[i-1] == -1 &amp;&amp; motes[i].getInterfaces().getPosition().getDistanceTo(motes[0]) &lt;= 50) {
//                 log.log("Mote " + (i+1) + " in range and scanning on channel: " + motes[i].getInterfaces().getRadio().getChannel() + "\n");
            }
        }   
//         log.log("----------------------------------------------------\n");
    }
    log.log(sim.getSimulationTimeMillis() + "\t ID:" + id + "\t" + msg + "\n");
	YIELD(); /* wait for another mote output */

}

log.testOK(); /* Report test success and quit */
//log.testFailed(); /* Report test failure and quit */</script>
      <active>true</active>
    </plugin_config>
    <width>1244</width>
    <z>1</z>
    <height>426</height>
    <location_x>1</location_x>
    <location_y>577</location_y>
  </plugin>
</simconf>

