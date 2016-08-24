#!/usr/bin/python
#python parser
import sys
import json
import subprocess
#Parse Args
# if len(sys.argv)!=2:
#     print "ERROR: Need a single argument."
#     print "   Usage: %s interface_state" % sys.argv[0]
#     exit(1)
#Collect Output
output=None

output=subprocess.check_output(['/usr/sbin/smonctl -j'],shell=True)

# if sys.argv[1] == "fan":
#     output=subprocess.check_output(['/usr/bin/netshow interface all -j'],shell=True)
# elif sys.argv[1] == "memory":
#     output=subprocess.check_output(['/usr/cumulus/bin/cl-netstat -j'],shell=True)
# else:
#     print "   Usage: %s interface_state" % sys.argv[0]
#     exit(1)
hostname=subprocess.check_output(['/bin/hostname'],shell=True).replace("\n","")
#Parse and Display Output
parsed_output=json.loads(output)

for item in parsed_output:
    print 'hwenv_state,host=%s,device=%s state="%s"' %(hostname,item['name'],item['state'])
    # print 'hwenv_state,host=%s,device=%s speed="%s"' %(hostname,item,parsed_output[item]['speed'])
    # print item;
exit(0)