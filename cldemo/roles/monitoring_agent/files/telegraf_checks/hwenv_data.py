#!/usr/bin/python

import json
import subprocess
from output_module import ExportData

"""
Collects HW Info
"""

def collect_data():
    output=None
    output=subprocess.check_output(['/usr/sbin/smonctl -j'],shell=True)
    parsed_output=json.loads(output)
    #data = ExportData(data_set_name,fixed_tags,variable_tags,data)
    data = ExportData("hwenv_state")

    for item in parsed_output:
        #data.add_row({variable_tags},{data})
        data.add_row({"device":item['name']},{"state":'"'+item['state']+'"'})
        if 'input' in item:
            data.add_row({"device":item['name']},{"input":item['input']})

    #Use this to sanity check the datastructure
    #data.show_data()

    #Send the data
    data.send_data("cli")

collect_data()

exit(0)
