#!/usr/bin/python
#python parser
import psutil
import sys
import json
import subprocess
# Parse Args
if len(sys.argv)!=2:
    print "ERROR: Need a single argument."
    print "   Usage: %s cpu|memory|disk" % sys.argv[0]
    exit(1)

#This module uses the psutil library to pull cpu, memory, disk.
# Collect Output
output=None

hostname=subprocess.check_output(['/bin/hostname'],shell=True).replace("\n","")

if sys.argv[1] == "cpu":
    output=psutil.cpu_percent(interval=None, percpu=True)
    print 'systemenv,host=%s,device=cpu cpu=%s' %(hostname,output)
elif sys.argv[1] == "memory":
    output=psutil.virtual_memory()
    print 'systemenv,host=%s,device=memused percent_used=%s' %(hostname,output.percent)
elif sys.argv[1] == "disk":
    output=psutil.disk_usage('/')
    print 'systemenv,host=%s,device=diskused percent_used=%s' %(hostname,output.percent)
else:
    print "   Usage: %s cpu|memory|disk" % sys.argv[0]
    exit(1)

#Parse and Display Output
# parsed_output=json.loads(output)

# for item in parsed_output:
#     print 'systemenv,host=%s,device=%s state="%s"' %(hostname,item['name'],item['state'])

#     if 'input' in item:
#         print 'hwenv_state,host=%s,device=%s input="%s"' %(hostname,item['name'],item['input'])
exit(0)