#!/usr/bin/python
#python parser
import sys
import json
import subprocess
#Parse Args
if len(sys.argv)!=2:
    print "ERROR: Need a single argument."
    print "   Usage: %s interface_state" % sys.argv[0]
    exit(1)
#Collect Output
output=None
if sys.argv[1] == "interface_state":
    output=subprocess.check_output(['/usr/bin/netshow interface all -j'],shell=True)
elif sys.argv[1] == "interface_stats":
    output=subprocess.check_output(['/usr/cumulus/bin/cl-netstat -j'],shell=True)
else:
    print "   Usage: %s interface_state" % sys.argv[0]
    exit(1)
hostname=subprocess.check_output(['/bin/hostname'],shell=True).replace("\n","")
#Parse and Display Output
parsed_output=json.loads(output)

if sys.argv[1] == "interface_state":
    for item in parsed_output:
        print 'iface_state,host=%s,interface=%s state="%s"' %(hostname,item,parsed_output[item]['linkstate'])
        print 'iface_state,host=%s,interface=%s speed="%s"' %(hostname,item,parsed_output[item]['speed'])
elif sys.argv[1] == "interface_stats":
    for item in parsed_output:
        print 'iface_stats,host=%s,interface=%s PKT_RX_OK="%s"' %(hostname,item,parsed_output[item]['PKT_RX_OK'])
        print 'iface_stats,host=%s,interface=%s PKT_TX_OK="%s"' %(hostname,item,parsed_output[item]['PKT_TX_OK'])
        print 'iface_stats,host=%s,interface=%s PKT_RX_DRP="%s"' %(hostname,item,parsed_output[item]['PKT_RX_DRP'])
        print 'iface_stats,host=%s,interface=%s PKT_TX_DRP="%s"' %(hostname,item,parsed_output[item]['PKT_TX_DRP'])
exit(0)