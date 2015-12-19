#!/usr/bin/env python
"""
 check-cumulus-sw-temp

 DESCRIPTION
   Check Cumulus Switch Temperatures

 OUTPUT
    plain text

 PLATFORMS:
    Hardware Switch running Cumulus Linux

 DEPENDENCIES:
    Python 2.7+

 USAGE:
   check-cumulus-sw-temp -w 85 -c 97

 ARGUMENTS:
   --critical: Critical threshold percentage.
               Set exit code to 2 if any temperature sensor is above the critical
               threshold. Default is 90
   -c: alias for --critical
   --warning: Warning threshold percentaged
              Set exit code to 1 if any temperature sensor is above the warning
              threshold. Default is 95
   -w: alias for --warning

 NOTES:

 TODO:
   Support More granular checks like CPU Temp Sensors or Inlet or Outlet Sensors
   Depends on how soon HW switch vendors standardize on a switch board layout

 LICENSE:
   Copyright 2015 Cumulus Networks
   Original Author: Stanley Karunditu <stanleyk@cumulusnetworks.com>
   Released under the the MIT license. see LICENSE for details.
"""

import argparse
import sys
import json
import subprocess


def check_temp(_args):
    """ Main function to check Switch temperature
    """
    try:
        cmd = '/usr/sbin/smonctl -j'.split()
        json_str = subprocess.check_output(cmd)
    except OSError as e:
        print("problem executing smonctl %s " % (e))
        exit(2)
    smon_output = json.loads(json_str)
    _msg = None
    _code = 0
    for _sensor in smon_output:
        if _sensor.get('type') == 'temp' and \
                _sensor.get('state') == 'OK':
            _max = float(_sensor.get('max'))
            _curr = float(_sensor.get('input'))
            _percent_diff = (_curr/_max) * 100
            if _args.critical and _percent_diff > _args.critical:
                _msg = "CRITICAL: %s - " % (_sensor.get('description')) + \
                    "Current:%s Max:%s Threshold:%s%%" % (_curr, _max, _args.critical)
                _code = 2
            elif _args.warning and _percent_diff > _args.warning:
                _msg = "WARNING: %s - " % (_sensor.get('description')) + \
                    "Current:%s Max:%s Threshold:%s%%" % (_curr, _max, _args.warning)
                _code = 1
    if _msg:
        print(_msg)
        exit(_code)


def print_help(parser):
    parser.print_help()
    exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Cumulus Switch Temp")
    parser.add_argument('-w', '--warning',
                        type=int,
                        metavar='PERCENT',
                        default=90,
                        help='Percent Warning Threshold for Switch Temp')
    parser.add_argument('-c', '--critical',
                        type=int,
                        default=90,
                        metavar='PERCENT',
                        help='Percent Critical Threshold for Switch Temp')
    if (len(sys.argv) < 2):
        print_help(parser)
    _args = parser.parse_args()
    check_temp(_args)
