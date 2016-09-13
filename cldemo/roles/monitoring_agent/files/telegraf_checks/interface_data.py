#!/usr/bin/python

import json
import subprocess
from output_module import ExportData

"""
Collects all interface info.
"""

def collect_data():
    output=None
    output=subprocess.check_output(['/usr/cumulus/bin/cl-netstat -j'],shell=True)
    parsed_output=json.loads(output)
    #data = ExportData(data_set_name,fixed_tags,variable_tags,data)
    data = ExportData("iface_info",{})

    for item in parsed_output:
        #data.add_row({variable_tags},{data})
        data.add_row({"interface":item},{"RX_OK":parsed_output[item]['RX_OK']})
        data.add_row({"interface":item},{"TX_OK":parsed_output[item]['TX_OK']})
        data.add_row({"interface":item},{"RX_DRP":parsed_output[item]['RX_DRP']})
        data.add_row({"interface":item},{"TX_DRP":parsed_output[item]['TX_DRP']})

    output=subprocess.check_output(['/usr/bin/netshow interface all -j'],shell=True)
    parsed_output=json.loads(output)

    for item in parsed_output:
        #data.add_row({variable_tags},{data})
        data.add_row({"interface":item},{"linkstate":'"'+parsed_output[item]['linkstate']+'"'})
        data.add_row({"interface":item},{"speed":'"'+parsed_output[item]['speed']+'"'})

    #Use this to sanity check the datastructure
    #data.show_data()

    #Send the data
    data.send_data("cli")

collect_data()

exit(0)
