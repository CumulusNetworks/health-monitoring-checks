#!/usr/bin/python
import psutil
import sys
import json
import subprocess
<<<<<<< HEAD
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
=======
from output_module import ExportData

"""
This module uses the psutil library to pull cpu, memory, disk.
"""

def usage():
>>>>>>> f7b4433ddb8182b9809a0a917cc2e705093d5d39
    print "   Usage: %s cpu|memory|disk" % sys.argv[0]
    exit(1)

def collect_data():
    #data = ExportData(data_set_name,fixed_tags,data)
    data = ExportData("systemenv",{},)

    output=None
    if sys.argv[1] == "cpu":
        output=psutil.cpu_percent(interval=None, percpu=True)
        #data.add_row({tag_name:tag_value,datapoint_name:datapoint_value}
        data.add_row({"device":"cpu","cpu":output[0]})

    elif sys.argv[1] == "memory":
        output=psutil.virtual_memory()
        #data.add_row({tag_name:tag_value,datapoint_name:datapoint_value}
        data.add_row({"device":"memused","percent_used":output.percent})

    elif sys.argv[1] == "disk":
        output=psutil.disk_usage('/')
        #data.add_row({tag_name:tag_value,datapoint_name:datapoint_value}
        data.add_row({"device":"diskused","percent_used":output.percent})
    else:
        usage()

    #Use this to sanity check the datastructure
    #data.show_data()

    #Send the data
    data.send_data("cli")

#Parse Args
if len(sys.argv)!=2:
    print "ERROR: Need a single argument."
    usage()

collect_data()

exit(0)
