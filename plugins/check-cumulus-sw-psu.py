#!/usr/bin/env python
"""
 This filename contains a health monitoring plugin which is still
 being developed and is still in the alpha testing stage.
 ----------------------------------------------------------------

 check-cumulus-sw-psu

 DESCRIPTION
   Check Cumulus Switch Power Supplies

 OUTPUT
    plain text

 PLATFORMS:
    Hardware Switch running Cumulus Linux.

 DEPENDENCIES:
    Python 2.7+

 USAGE:
   check-cumulus-sw-psu --min-psu 2

 ARGUMENTS:
   --min-psu: Minimum number of PSU units before an alert is set

 NOTES:

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


def check_psu(_args):
    """ Main function to check Fan speed
    """
    try:
        cmd = '/usr/sbin/smonctl -j'.split()
        json_str = subprocess.check_output(cmd)
    except OSError as e:
        print("problem executing smonctl %s " % (e))
        exit(2)
    smon_output = json.loads(json_str)
    psu_count = 0
    for _sensor in smon_output:
        if _sensor.get('type') == 'power' and \
                _sensor.get('state') == 'OK':
            psu_count += 1
            if psu_count < _args.min_psu:
                _msg = "CRITICAL: Power Supply Count Low - Current:%s Threshold:%s" \
                    % (psu_count, _args.min_psu)
                print(_msg)
                exit(2)


def print_help(parser):
    parser.print_help()
    exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Cumulus Switch PSUs")
    parser.add_argument('--min-psu',
                        type=int,
                        metavar='NUMBER',
                        help='Minimum number of PSUs')

    if (len(sys.argv) < 2):
        print_help(parser)
    _args = parser.parse_args()
    check_psu(_args)
