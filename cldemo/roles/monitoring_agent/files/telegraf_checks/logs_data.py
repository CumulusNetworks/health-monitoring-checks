from pygtail import Pygtail
import sys
from output_module import ExportData
from socket import gethostname


"""
Collects log information and uploads it as a metric.
Uses the pygtail library which is installed via pip
"""


def parse_logs():
    data = ExportData("logs")
    reason = ""
    peer = ""

    for line in Pygtail("/var/log/syslog"):
        # print line
        if "sent to neighbor" in line:
            reason = line.split('(')[1].split(')')[0]
        if "Down BGP Notification" in line:
            # print "***found*** " + '"'+str(line.split(' ')[5])+'"'
            peer = line.split(' ')[5]
        if len(reason) > 0 and len(peer) > 0:
            data.add_row({"msg":"log"},{"reason":'"'+reason+" on "+gethostname()+" from "+peer+'"',"peer":'"'+peer+'"'})
            reason = ""
            peer = ""

    # data.show_data()
    data.send_data("cli")

parse_logs()

exit(0)