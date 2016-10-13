import sys
import imp
sys.path.append('/home/jkopp/git/ucs-jaguar-test-fork/src')
sys.path.append('/home/jkopp/git/gate-src/src')


try:
    imp.find_module('pytest')
except ImportError:
    print ("Pytest module is not found.  Are you running from within Orchestrator?")
    exit()
from modules.devices.gate_device import Device
from utils import common_maint_fixtures as step_maint
from modules.api import gate_orchestratorapi as host_api
from modules.cli.gate_dockercli import DockerCLI as dcli
from modules.cli.gate_linuxcli import LinuxCLI
from modules.api.gate_seleniumapi import *

 
dockerClient = dcli.UBUNTU_CLIENT_IMAGE
#dockerClient = dcli.UBUNTU_FIREFOX_IMAGE
global host
global cli_container_info
global cli_container

#def init():
cfg_file = "/home/jkopp/git/ucs-jaguar-test-fork/test-handler-06.cfg"
host = Device(from_file=cfg_file, device='host')

cli_container_info = {'name': 'cli-client1',
                   'prompt':'root@cli-client1:[\w~\/]+#',
                   'intf':'eth1',
                   'veth_link':('gate_vout', 'gate_vin'),
                   'brname':'int-maint'}
cli_container = dcli(name=cli_container_info['name'],
                   prompt=cli_container_info['prompt'])

#def teardown():
'''
    try:
            cli_container.send_cmd('dhclient -r {}'.format(
                                cli_container_info['intf']))
    except Exception as  e:
            print "Exception during dhcp release for maintenance container: {}"\
                .format(str(e))
    try:
        cli_container.logout()
    except Exception as e:
        print "Exception during logging out from maintenance container: {}"\
              .format(str(e))
'''
try:
    host_api.remove_wired_link(brname=cli_container_info['brname'], veth_link=
                               cli_container_info['veth_link'])
except Exception as e:
    print "Exception while removing link/bridge: {}".format(str(e))

'''
try:
    cli_container.remove_container(force_remove=True)
except Exception as e:
    print "Exception while removing maintenance container: {}"\
            .format(str(e))
'''

#def setup():
cli_container.run_container(image=dockerClient)
cli_container.login()
host_api.add_wired_link(brname=cli_container_info['brname'],
                        host_ifname=host.maint_link,
                        ctrname=cli_container.name,
                        ctr_ifname=cli_container_info['intf'],
                        veth_link=cli_container_info['veth_link'])

cli_container.send_cmd('dhclient {}'.format(cli_container_info['intf']))
op1 = cli_container.send_cmd('ifconfig {}'.format(cli_container_info['intf']))

if 'inet addr:172.20.1.' in str(op1):
    print("Successfully received IP")
else:
    print("IP was not as expected, received IP: " + op1)
    assert False, "Failed to receive expected IP address"

"""
if __name__ ==  '__main__':
    init()
    #Teardown any pre-existing infrastructere
    teardown()
    setup()
"""
