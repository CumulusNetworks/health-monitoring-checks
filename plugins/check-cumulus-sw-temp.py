#!/usr/bin/env python
"""
 check-cumulus-sw-temp

 DESCRIPTION
   Check Cumulus Switch Temperatures. Alerts based on
   numbers provided in smonctl -v. There is the 'max' value
   which maps to a warning. and the 'crit' value which maps
   to a critical alert.

 OUTPUT
    plain text

 PLATFORMS:
    Hardware Switch running Cumulus Linux

 DEPENDENCIES:
    Python 2.7+

 USAGE:
   check-cumulus-sw-temp

 ARGUMENTS:
     None

 NOTES:
     Smonctl provides a warning (max) and critical (crit) threshold
     level output in its output.
     Use this as a guide to generate a warning and critical message.
     Warning message is issued when current Temp is less than 2 degrees of
     max (warning) temp level
     Critical message is issued when current Temp is less than 2 degrees of
     crit (critical) temp level.
     When the switch reaches critical level it shuts down.

 TODO:
   Support More granular checks like CPU Temp Sensors or Inlet or Outlet Sensors
   Depends on how soon HW switch vendors standardize on a switch board layout

 LICENSE:
   Copyright 2015 Cumulus Networks
   Original Author: Stanley Karunditu <stanleyk@cumulusnetworks.com>
   Released under the the MIT license. see LICENSE for details.
"""

import argparse
import json
import subprocess


def check_temp():
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
            _crit = float(_sensor.get('crit'))
            _max = float(_sensor.get('max'))
            _curr = float(_sensor.get('input'))
            _send_warn = (_max - _curr) < 2
            _send_crit = (_crit - _curr) < 2
            if _send_crit:
                _msg = "CRITICAL: %s - " % (_sensor.get('description')) + \
                    "Current:%s Threshold:%s " % (_curr, _crit)
                _code = 2
            elif _send_warn:
                _msg = "WARNING: %s - " % (_sensor.get('description')) + \
                    "Current:%s Threshold:%s" % (_curr, _max)
                _code = 1
    if _msg:
        print(_msg)
        exit(_code)


def print_help(parser):
    parser.print_help()
    exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Cumulus Switch Temp. Alerts when temp is within 2% " +
        "of warning(max) or critical(crit) levels defined in 'smonctl -v' output")
    _args = parser.parse_args()
    check_temp()
