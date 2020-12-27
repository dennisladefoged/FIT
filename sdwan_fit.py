#!/usr/bin/env python3
import os
import random
import socket
import re

fitOptions = ['appctrl', 'webtraffic']


#clear screen
os.system('clear')

#obtain default gateway, interface, ip_address ,subnet and original mac

get_gateway = os.popen('netstat -r | grep default  | awk {\'print $2\'}')
gateWay=get_gateway.read().strip()
#print(gateWay)

get_interface = os.popen('netstat -r | grep default  | awk {\'print $8\'}')
interface=get_interface.read().strip()
#print(interface)

get_ipaddr = os.popen('ifconfig '+interface+' | grep inet | awk \'NR==1{print $2}\'')
ipaddr=get_ipaddr.read().strip()
#print(ipaddr)

network = re.sub("\d{1,3}$","",ipaddr)
#print (network)

get_mac = os.popen('ifconfig '+interface+' | grep ether | awk {\'print $2\'}')
original_mac=get_mac.read().strip()
#print (original_mac)

lower = int(100)
upper = int(150)


def random_bytes(num=6):
    return [random.randrange(256) for _ in range(num)]

def generate_mac(uaa=False, multicast=False, oui=None, separator=':', byte_fmt='%02x'):
    mac = random_bytes()
    if oui:
        if type(oui) == str:
            oui = [int(chunk) for chunk in oui.split(separator)]
        mac = oui + random_bytes(num=6-len(oui))
    else:
        if multicast:
            mac[0] |= 1 # set bit 0
        else:
            mac[0] &= ~1 # clear bit 0
        if uaa:
            mac[0] &= ~(1 << 1) # clear bit 1
        else:
            mac[0] |= 1 << 1 # set bit 1
    return separator.join(byte_fmt % b for b in mac)


loopvar = 1

while loopvar<51 :


#       Generate a random 4th octet and join to subnet
        ip = network+"".join(str(random.randint(lower, upper)))
#       Generate new mac
        newmac = generate_mac(uaa=True)
#       Assign MAC & IP to interface
        os.system('ifconfig '+interface+' down')
        os.system('ifconfig '+interface+' hw ether '+generate_mac(uaa=True))
        os.system('ifconfig '+interface+' '+ip+' netmask 255.255.255.0')
        os.system('route add default gw '+gateWay)
        os.system('ifconfig '+interface+' up')
        print('=============================')
        print ('Iteration Number '+str(loopvar)+' of 50')
        print ('Using the IP: '+ip)
        print ('Run FIT with the option: appctrl')
#       Start FIT with appctlr
        os.system('cd /home/fit/ && ./fit.py appctrl')
        loopvar=loopvar+1
else :
#       Assign Original MAC and renew dhcp
        os.system('ifconfig '+interface+' down')
        os.system('ifconfig '+interface+' hw ether '+original_mac)
        os.system('dhclient '+interface+' -r')
        os.system('ifconfig '+interface+' up') 
        os.system('dhclient '+interface) 
