#!/usr/bin/python

import json
import subprocess
from output_module import ExportData

"""
Collects LLDP Neighbor count.
"""

def collect_data():
    output=None
    output=subprocess.check_output(['sudo /usr/sbin/lldpctl -f json'],shell=True)
    
    parsed_output=json.loads(output)
    #data = ExportData(data_set_name,fixed_tags,variable_tags,data)
    data = ExportData("lldp_state",data={"neighbors":len(parsed_output['lldp'][0]['interface'])})

    #Use this to sanity check the datastructure
    #data.show_data()

    #Send the data
    data.send_data("cli")

collect_data()

exit(0)
