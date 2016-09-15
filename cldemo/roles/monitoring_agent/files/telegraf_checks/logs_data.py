from pygtail import Pygtail
import sys
from output_module import ExportData

"""
Collects log information and uploads it as a metric
"""


def parse_logs():
    data = ExportData("logs")

    for line in Pygtail("/var/log/syslog"):
        # print line
        if "sent to neighbor" in line:
            data.add_row({"msg":"log"},{"peer":'"'+str(line.split('(')[1].split(')'))+'"'})
        if "Down BGP Notification" in line:
            # print "***found*** " + '"'+str(line.split(' ')[5])+'"'
            data.add_row({"msg":"log"},{"peer":'"'+str(line.split(' ')[5])+'"',"reason":"Hold Timer Expired?"})

    data.show_data()
    data.send_data("cli")

parse_logs()

exit(0)