"""
pointToGateBSG.py

This module is a helper file that edits lruprofile.json to point to GATE-BSG, then reboots the LRU.

Example:
    $ python pointToGateBSG.py 1

Args:
    test_handler_number - The test handler number that the LRU is connected to.

The "handler_number" parameter will be used to derive the test-handler...cfg file to be used by this script to connect
to the LRU, and will determine the GATE-BSG port number that the lruprofile will be pointng to.

This module is expected to be copied to the ucs-jaguar-test root directory.

:Author: Jonathan Kopp

"""
import time
import datetime
import io
import os
from modules.devices.gate_device import Device
from utils import cleanup_functions
#from utils import common_maint_fixtures as step_maint
from modules.api import gate_orchestratorapi as host_api
from modules.cli.gate_dockercli import DockerCLI as dcli
from modules.cli.gate_linuxcli import LinuxCLI
#from modules.api.gate_seleniumapi import *


#global testConfigDir
#global configTarFile
#global acmIP
#global username
#global password
#password = "gogopassword"
#username = "gogo"
#newSSID = "acmTestWifi"
#testConfigDir = "/root/testAcmConfig"
#configTarFile = "jaguar.tar.gz"
#acmIP = "192.168.1.250"
              
def edit_congif_file(jsonFile, nodejsScript):
    testJavaScriptDir = "/root/javaScript/"
    lru_cli.send_cmd("rm -rf " + testJavaScriptDir)
    lru_cli.send_cmd("mkdir -p " + testJavaScriptDir)
    lru_cli.send_cmd("cd " + testJavaScriptDir)
    lru_cli.send_cmd("echo \"" + nodejsScript + "\" > script.js")
    lru_cli.send_cmd("chmod 755 script.js")
    lru_cli.send_cmd("/bin/node script.js " +  jsonFile)
    lru_cli.send_cmd("rm -rf " + testJavaScriptDir)

decreaseSchemaVersion = """
    var fileName = process.argv[2];
    //TODO add file check for argv[2]
    var fs = require('fs')
    var schemaID = 'schema-version'
    var content = require(fileName)
    for (var i = 0, length = content.length; i < length; i++) {
	    if ( content[i]._id.toString() === schemaID) {
    	        content[i].value = parseInt(content[i].value) - 1
	    }
    }
    fs.writeFileSync(fileName, JSON.stringify(content, null, 2));
    console.log('success')
"""

def edit_config_file(jsonFile, nodejsScript):
    #Create clean copy script directory
    testJavaScriptDir = "/root/javaScript/"
    lru_cli.send_cmd("rm -rf " + testJavaScriptDir)
    lru_cli.send_cmd("mkdir -p " + testJavaScriptDir)
    lru_cli.send_cmd("pushd " + testJavaScriptDir)
    lru_cli.send_cmd("echo \"" + nodejsScript + "\" > script.js")
    lru_cli.send_cmd("chmod 755 script.js")
    retVal = lru_cli.send_cmd("/bin/node script.js " +  jsonFile)
    assert "success" in retVal, "Error in editing JSON config file: " + jsonFile
    lru_cli.send_cmd("rm -rf " + testJavaScriptDir)
    lru_cli.send_cmd("popd ")

def reboot():
    try:
        lru_cli.send_cmd("reboot")
    except Exception as e:
        if 'TIMEOUT' in str(e):
            print("Current session might have disconnected upon reboot")
        else:
            raise Exception("Non-timeout exception upon reinstall: ", e)

    time_to_wait = 600
    cmd_ping = 'ping -c 1 172.20.1.1'
    st = time.time()
    while((time.time() - st) < time_to_wait):
        print (cmd_ping)
        if ', 0% packet loss' in client_ctr.send_cmd(cmd_ping):
            print ("After reboot, pings to LRU succeeded after {} seconds"
                   .format(time.time()-st))
            return True 
        time.sleep(1)
    return False

def resetLRU():
    sessionId = client_ctr.send_cmd("date +'%H%M%S'")
    lru_cli.login(session_id=sessionId, timeout=60)
    lru_cli.send_cmd("jag config factory")
    lru_cli.send_cmd("jag sys save")
    

def connect(cfg_file):
    """
    Connects this docker session with the LRU.
    
    """

    #cleanup_functions.main()

    #Set up docker container with Firefox browser linked to LRU maintanence
    # port
    global host
    host = Device(from_file=cfg_file, device='host')
    global client_ctr_info
    client_ctr_info = {'name': 'ff-client1',
                          'prompt':'root@ff-client1:[\w~\/]+#',
                          'intf':'eth1',
                          'veth_link':('gate_vout', 'gate_vin'),
                          'brname':'int-maint'}
    global client_ctr
    client_ctr = dcli(name=client_ctr_info['name'],
               prompt=client_ctr_info['prompt'])
    client_ctr.run_container(image=dcli.UBUNTU_FIREFOX_IMAGE)
    client_ctr.login()
    host_api.add_wired_link(brname=client_ctr_info['brname'],
                            host_ifname=host.maint_link,
                            ctrname=client_ctr.name,
                            ctr_ifname=client_ctr_info['intf'],
                            veth_link=client_ctr_info['veth_link'])

    client_ctr.send_cmd('dhclient {}'.format(client_ctr_info['intf']))
    op1 = client_ctr.send_cmd('ifconfig {}'.format(client_ctr_info['intf']))

    if 'inet addr:172.20.1.' in str(op1):
        print("Successfully received IP")
    else:
        print("IP was not as expected, received IP: " + op1)
        assert False, "Failed to receive expected IP address"
    # Set up cli session on LRU inside of docker client container
    jaguar_info = Device(from_file=cfg_file, device='jaguar')
    global lru_cli
    lru_cli = LinuxCLI(hostname=jaguar_info.hostname,
                          domain=jaguar_info.domain,
                          username=jaguar_info.username,
                          password=jaguar_info.password,
                          prompt=jaguar_info.prompt, handler=client_ctr)
    
def setup_function(function):
    """Setup:

    #. Access the LRU's maintenance GUI
    #. Restore to factory default settings.
    #. Set up a temporary test directory on the LRU by executing `mkdir testAcmConfig`
       on the LRU's CLI.

    """
    resetLRU()
    assert reboot(), "LRU failed to come up after 600 seconds after reboot"




def teardown():
    """Teardown Steps:
    
    #. Reset LRU to factory default settings.
    #. Disconnect the laptop from the LRU's maintenance port.

    """
    logger.debug("Starting teardown.")

    #Teardown docker container
    try:
            client_ctr.send_cmd('dhclient -r {}'.format(
                                  client_ctr_info['intf']))
    except Exception as  e:
        logger.debug("Exception during dhcp release for maintenance container: {}".format(str(e)))
    try:
        client_ctr.logout()
    except Exception as e:
        logger.debug("Exception during logging out from maintenance container: {}".format(str(e))

    try:
        host_api.remove_wired_link(brname=client_ctr_info['brname'], veth_link=
        client_ctr_info['veth_link'])
    except Exception as e:
        logger.debug("Exception while removing link/bridge: {}".format(str(e)))
    try:
        client_ctr.remove_container(force_remove=True)
    except Exception as e:
        logger.debug("Exception while removing maintenance container: {}".format(str(e)))

    logger.debug("Teardown completed.")


def main():

    acmFile = testConfigDir + "/var/jaguar/configs/active/systems.json"
    
    # Get a defualt configuration value:
    ff_browser = Browser("Firefox", "http://wizard.gogo.aero", remote_ip_addr=
                      '0.0.0.0', header_title='Jaguar')
    assert ff_browser != None
    ff_browser.click_element("index-menu-a-radios")
    ff_browser.click_element("radios-security-div-radio1Name")
    defaultSSID=ff_browser.get_element_text("radios-security-input-radio1Ssid")

            
    # Change the LRU configuration and save it.
    ff_browser.enter_text("radios-security-input-radio1Ssid", "acmTestSSID")
    ff_browser.click_element("menu-saveConfig-button-save")
    time.sleep(10)
    ff_browser.click_element("menu-restart-button-restart")
    time.sleep(10)
    ff_browser.close_browser()
            
    # Wait for LRU to reboot.
    rebootStatus = False
    time_to_wait = 600
    cmd_ping = 'ping -c 1 172.20.1.1'
    st = time.time()
    while((time.time() - st) < time_to_wait):
        print (cmd_ping)
        if ', 0% packet loss' in client_ctr.send_cmd(cmd_ping):
            print ("After reboot, pings to LRU succeeded after {} seconds"
                   .format(time.time()-st))
            rebootStatus = True 
            break
        time.sleep(1)
    assert rebootStatus, ("LRU failed to come up after {} seconds after reboot".format(time_to_wait))
    
    
    # Set the schema version of ACM and local configuration to a lower value
    sessionId = 'test_acm_{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
    lru_cli.login(session_id=sessionId, timeout=60)
    lru_cli.send_cmd("cd ")
    lru_cli.send_cmd("chmod 600 .netrc") 
    lru_cli.send_cmd("cd " + testConfigDir)
    lru_cli.send_cmd("echo -en 'open " + acmIP + "\nget " + configTarFile + 
                        "\nbye' > ftpGet.cmd") 
    lru_cli.send_cmd("ftp < ftpGet.cmd")
    lru_cli.send_cmd("tar xzf " + configTarFile)
    edit_config_file(acmFile, decreaseSchemaVersion)
    lru_cli.send_cmd("tar -czf " + configTarFile + " var")
    lru_cli.send_cmd("curl -n -s --connect-time 15 --max-time 30 -T " + 
                  configTarFile + " ftp://" + acmIP)

    # Reboot LRU
    assert reboot(), ("LRU failed to come up after {} seconds after reboot".format(time_to_wait))
        
        
    #. Verify that the LRU runs from the factory defualt schema configuration.
    ff_browser = Browser("Firefox", "http://wizard.gogo.aero", remote_ip_addr=
                          '0.0.0.0', header_title='Jaguar')
    assert ff_browser != None
    ff_browser.click_element("index-menu-a-radios")
    ff_browser.click_element("radios-security-div-radio1Name")
    ssid = ff_browser.get_element_text("radios-security-input-radio1Ssid")
    assert ssid == defaultSSID


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print "usage: python pointToGateBSG.py <test handler number> "
        sys.exit(1)
    configFile = "test-handler-0" + sys.argv[1] + ".cfg"
    if not os.path.isfile(configFile):
        print "Error: Could not find " + configFile + " in working directory."
        sys.exit(1)

    logger.debug("Connecting to LRU with ", configFile , " ...")
    connect(configFile)
    teardown()
