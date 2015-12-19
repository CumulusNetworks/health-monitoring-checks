#!/usr/bin/env python
"""
 check-cumulus-sw-fans

 DESCRIPTION
   Check Cumulus Switch Fan Speeds and Fan Status

 OUTPUT
    plain text

 PLATFORMS:
    Hardware Switch running Cumulus Linux.

 DEPENDENCIES:
    Python 2.7+

 USAGE:
   check-cumulus-sw-fans -w 85 -c 97 --min-fans 5

 ARGUMENTS:
   --critical: Critical threshold percentage.
               Set exit code to 2 if any fan speed is above the critical
               threshold
   -c: alias for --critical
   --warning: Warning threshold percentaged
              Set exit code to 1 if any fan speed is above the warning
              threshold
   -w: alias for --warning
   --min-fans: Minimum number of fans running before a critical event is generated

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


def check_fans(_args):
    """ Main function to check Fan speed
    """
    try:
        cmd = '/usr/sbin/smonctl -j'.split()
        json_str = subprocess.check_output(cmd)
    except OSError as e:
        print("problem executing smonctl %s " % (e))
        exit(2)
    smon_output = json.loads(json_str)
    fan_count = check_fan_speeds(smon_output)
    if fan_count < _args.min_fans:
        _msg = "CRITICAL: Fan may be DOWN - Current:%s Min:%s" \
            % (fan_count, _args.min_fans)
        print(_msg)
        exit(2)


def check_fan_speeds(smon_output):
    _msg = None
    _code = 0
    fan_count = 0
    for _sensor in smon_output:
        if _sensor.get('type') == 'fan' and \
                _sensor.get('state') == 'OK' and not \
                _sensor.get('name').startswith('PSU'):
            fan_count += 1
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
    return fan_count


def print_help(parser):
    parser.print_help()
    exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Cumulus Switch Fans")
    parser.add_argument('-w', '--warning',
                        type=int,
                        metavar='PERCENT',
                        default=90,
                        help='Percent Warning Threshold for Switch Fan Speed')
    parser.add_argument('-c', '--critical',
                        type=int,
                        metavar='PERCENT',
                        default=95,
                        help='Percent Critical Threshold for Switch Fan Speed')
    parser.add_argument('--min-fans',
                        type=int,
                        metavar='NUMBER',
                        help='Minimum number of Fans')

    if (len(sys.argv) < 2):
        print_help(parser)
    _args = parser.parse_args()
    check_fans(_args)
