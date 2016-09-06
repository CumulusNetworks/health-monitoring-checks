#!/usr/bin/python
import psutil
import sys
import json
import subprocess
from output_module import ExportData

#This module uses the psutil library to pull cpu, memory, disk.
# Install required dependencies:
# sudo apt-get install gcc python-dev python-pip
# pip install psutil
# https://github.com/giampaolo/psutil/blob/master/INSTALL.rst

# Collect Output
output=None

hostname=subprocess.check_output(['/bin/hostname'],shell=True).replace("\n","")

"""
This module uses the psutil library to pull cpu, memory, disk.
"""

def usage():
    print "   Usage: %s cpu|memory|disk" % sys.argv[0]
    exit(1)

def collect_data():
    #data = ExportData(data_set_name,fixed_tags,variable_tags,data)
    data = ExportData("systemenv")

    output=None
    if sys.argv[1] == "cpu":
        output=psutil.cpu_percent(interval=None, percpu=True)
        #data.add_row({variable_tags},{data})
        data.add_row({"device":"cpu"},{"cpu":output[0]})

    elif sys.argv[1] == "memory":
        output=psutil.virtual_memory()
        #data.add_row({variable_tags},{data})
        data.add_row({"device":"memused"},{"percent_used":output.percent})

    elif sys.argv[1] == "disk":
        output=psutil.disk_usage('/')
        #data.add_row({variable_tags},{data})
        data.add_row({"device":"diskused"},{"percent_used":output.percent})
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
