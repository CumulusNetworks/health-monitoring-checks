#!/usr/bin/env python
"""
 check-bgp-routes

 DESCRIPTION
    Check BGP Route Count

 OUTPUT
    plain text

 PLATFORMS:
    Linux
    Cumulus Quagga
    Cumulus python-clcmd

 DEPENDENCIES:
    Python 2.7+

 USAGE:
   check-bgp-route-count --min-routes 3

 ARGUMENTS:
     --min-routes (Required): Minimum number of routes that should
     appear in the BGP route table. If the number is loweri or equal
     to this number then a critical alert is issued. Default is 0,
     meaning that BGP has lost all its routes.

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


def check_bgp_routes(_args):
    """ Main function to check bgp peers
    """
    try:
        cmd = 'sudo /usr/bin/cl-bgp route show json'.split()
        json_str = subprocess.check_output(cmd)
    except OSError as e:
        print("problem executing cl-bgp %s " % (e))
        exit(2)
    _output = json.loads(json_str)
    _routes = _output.get('routes').keys()
    _routelength = len(_routes)
    if _routelength <= _args.min_routes:
        print("Number of BGP Routes Too Low - " +
              "%s Threshold:%s" % (_routelength, _args.min_routes))


def print_help(parser):
    parser.print_help()
    exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Quagga BGP Route Count")
    parser.add_argument('-m', '--min-routes',
                        type=int,
                        default=0,
                        metavar='NUMBER',
                        help='Min number of routes before issuing critical ' +
                        'alert')

    if (len(sys.argv) < 2):
        print_help(parser)
    _args = parser.parse_args()
    check_bgp_routes(_args)
