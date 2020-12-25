#!/usr/bin/env python3.5
import os
import random
import socket

groups = ['staff', 'students']
fitOptions = ['appctrl', 'appctrl', 'appctrl', 'iprep', 'webtraffic', 'webtraffic', 'webtraffic','webtraffic', 'wf', 'wf', 'wf', 'wf', 'malwareurls']

#Create array with username from external file called "usernames.txt"
usersDB = [line.rstrip('\n') for line in open('/home/FIT-master/usersDB.txt')]

#clear screen
os.system('clear')

#obtain subnet from user
i = "n"
if i=="n":
        while i == "n":
                network = input("Please enter a /24 network to use (e.g. 192.168.1.): ")
                gateWay = input("Please enter the default gateway to use: ")
                lower = int(input("Please enter lower limit for 4th octet to use (1-254): "))
                upper = int(input("Please enter upper limit for 4th octet to use (1-254): "))
                print('You entered: '+network+'('+str(lower)+'-'+str(upper)+'). Gateway: '+gateWay)
                i = input ("Is this correct? (y/n): ")

elif i!="y":
        i = input ("Please enter 'y' or 'n': ")


print('Begin infinite loop')
print('===================')

loopvar = 1
while (loopvar):

        print('Press Ctrl + Z to stop')

#       Generate a random 4th octet and join to subnet
        ip = network+"".join(str(random.randint(lower, upper)
        ))
#       Assign IP to interface
        os.system('sudo ifconfig eth0 down')
        os.system('sudo ifconfig eth0 '+ip+' netmask 255.255.255.0')
        os.system('sudo route add default gw '+gateWay)
        os.system('sudo ifconfig eth0 up')

#       Select random user and group
        userName = random.choice(usersDB)
        groupName = random.choice(groups)

#       Generate LOGIN RADIUS ACCOUNTING INFO
        rad_in = "User-Name="+userName+",Calling-Station-ID="+userName+",Framed-IP-Address="+ip+",Class="+groupName+",Acct-Status-Type=Start"

        print ('=====================')
        print ('Sign in as: '+userName)
        print ('In group: '+groupName)
        print ('With IP Address: '+ip)
#       print ('RAD_IN is: '+rad_in)
        print ('=====================')

#       Send LOGIN to FGT using RADIUS ACCOUNTING
        os.system('echo '+rad_in+' | /usr/local/bin/radclient -q '+gateWay+' acct fortinet')

        j = random.randint(1,5)
        if j == 5:
                os.system('/home/FIT-master/fit.py vxvault')

#       print ('j = '+str(j))
        for k in range (random.randint(1,5)):
        #       Select a random FIT action
                fitSelect = random.choice(fitOptions)
                print ('Run FIT with the option: '+fitSelect)
        #       Start FIT
                os.system('/home/FIT-master/fit.py '+fitSelect)

#       Generate LOGOUT RADIUS ACCOUNTING INFO
        rad_out = "User-Name="+userName+",Calling-Station-ID="+userName+",Framed-IP-Address="+ip+",Class="+groupName+",Acct-Status-Type=Stop"

        print ('=====================')
        print ('Signing Out!!!')
        print ('=====================')

#       Send LOGOUT to FGT using RADIUS ACCOUNTING
        os.system('echo '+rad_out+' | /usr/local/bin/radclient '+gateWay+' acct fortinet')
