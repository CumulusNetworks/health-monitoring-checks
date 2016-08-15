#!/usr/bin/env python2.7

# Note: You can't run this in the same folder (network_common/files) as ujson.so.
# Python will try to load the .so and it will fail since it was built for CL

import subprocess
import ujson
import socket

sudo = "/usr/bin/sudo"
vtysh = "/usr/bin/vtysh"
netshow = "/usr/bin/netshow"


def run_json_command(command):
    """
    Run a command that returns json data. Takes in a list of command arguments
    :return: JSON string output from command
    """
    json_str = ''
    try:
        json_str = subprocess.check_output(command)
    except OSError as e:
        print("problem executing vtysh %s " % (e))
        exit(3)

    return json_str


def interface_data():

    # Gather output of interfaces

    interface_data_output = run_json_command(
        [sudo, netshow, "interface", "all", "-j"])

    # if bgp is not configured no output is returned
    if len(interface_data_output) == 0:
        print("No interface output. Is the hardware detected properly?")
        exit(3)

    json_interface_data = ujson.loads(interface_data_output.decode('utf-8'))

    if len(json_interface_data) == 0:
        print("No interfaces configured. Are any interfaces configured?")
        exit(3)

    # BGP is configured and peers exist.

    for interface in json_interface_data.keys():
        # print(interface)
        print("intstat,host=" + socket.gethostname() + ",interface=" + interface + " " + json_interface_data[interface]["linkstate"])


if __name__ == "__main__":

    interface_data()

    exit(0)
