from pygtail import Pygtail
import sys
from output_module import ExportData


tmp_output = []
tmp_line = ""



def parse_logs():
    data = ExportData("logs")
    for line in Pygtail("/var/log/syslog"):
        print line
        if "Down BGP Notification" in line:
            print "found again" + line
            data.add_row = [{"msg":"log"},{"peer":'"'+str(line.split(' ')[5])+'"',"reason":"Hold Timer Expired?"}]
        # sys.stdout.write(line)
    data.send_data("cli")

parse_logs()

exit(0)