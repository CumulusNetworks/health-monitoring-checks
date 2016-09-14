from pygtail import Pygtail
import sys

for line in Pygtail("/var/log/syslog"):
    if "session closed" in line:
        sys.stdout.write(line)

    # sys.stdout.write(line)