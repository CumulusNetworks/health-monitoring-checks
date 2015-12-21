#!/usr/bin/env python
"""
 check-bgp-peers

 DESCRIPTION
    Check BGP Peer Established Status and Count

 OUTPUT
    plain text

 PLATFORMS:
    Linux
    Cumulus Quagga
    Cumulus python-clcmd

 DEPENDENCIES:
    Python 2.7+

 USAGE:
   check-bgp-peers.py --min-down-peers 3

 ARGUMENTS:
     --min-down-peers (Required): Minimum number of peers down peers
     before sending a critical alert.

 NOTES:
     Make sure to install the user that executes this script to sudoers
     For example in the case of sensu. cl-bgp executable needs
     sudo privileges to run

     "sensu ALL = NOPASSWD: /usr/bin/cl-bgp"

 TODO:

 LICENSE:
   Copyright 2015 Cumulus Networks
   Original Author: Stanley Karunditu <stanleyk@cumulusnetworks.com>
   Released under the the MIT license. see LICENSE for details.
"""

import argparse
import sys
import json
import subprocess


def check_bgp_peers(_args):
    """ Main function to check bgp peers
    """
    try:
        cmd = 'sudo /usr/bin/cl-bgp summary show json'.split()
        json_str = subprocess.check_output(cmd)
    except OSError as e:
        print("problem executing cl-bgp %s " % (e))
        exit(2)
    _output = json.loads(json_str)
    _neighbors = _output.get('peers')
    _peers_not_working_count = 0
    for _peer, _peerstats in _neighbors.items():
        if _peerstats.get('state') != 'Established':
            _peers_not_working_count += 1

    if _peers_not_working_count >= _args.min_down_peers:
        print("CRITICAL: Number of Non Established BGP Peers - %s Threshold: %s"
              % (_peers_not_working_count, _args.min_down_peers))


def print_help(parser):
    parser.print_help()
    exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Quagga BGP Peers")
    parser.add_argument('-m', '--min-down-peers',
                        type=int,
                        metavar='NUMBER',
                        help='Number of non-established BGP peers ' +
                        'needed to generate an alert')

    if (len(sys.argv) < 2):
        print_help(parser)
    _args = parser.parse_args()
    check_bgp_peers(_args)
