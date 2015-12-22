#!/usr/bin/env python
"""
 This filename contains a health monitoring plugin which is still
 being developed and is still in the alpha testing stage.
 ----------------------------------------------------------------

 check-memory

 DESCRIPTION
   Check Memory Usage either based on free memory or used memory

 OUTPUT
    plain text

 PLATFORMS:
    Linux

 DEPENDENCIES:
    Python 2.7+

 USAGE:
   check-memory.py -w 80 -c 90

 ARGUMENTS:
   --warning:  Percent Memory usage beyond which an exit code of 1 is returned
   -w: alias for --warning
   --critical: Percent Memory usage beyond which an exit code of 2 is returned
   -c: alias for --critical
   --free: Calculate percent memory usage based on amount of free memory left
   --used: Calculate percent memory usage based on used memory left. This is the
    default calculation.

 NOTES:
   Derived from check-ram.rb from sensu-plugins repository. Converted to Python - stanleyK

 TODO:

 LICENSE:
   Copyright 2015 Cumulus Networks
   Original Author: Stanley Karunditu <stanleyk@cumulusnetworks.com>
   Released under the the MIT license. see LICENSE for details.
"""

import argparse
import subprocess


def check_memory(_args):
    total = None
    used = None
    try:
        cmd = "/usr/bin/free -m".split()
        _output = subprocess.check_output(cmd)
        _line = _output.split('\n')[1]
        _splitline = _line.split()
        (total, used) = float(_splitline[1]), float(_splitline[2])
    except OSError as e:
        print("problem executing Free %s " % (e))
        exit(2)
    if _args.free:
        _freemem_percent = (total - used) / 100
        if _args.critical and _args.critical > _freemem_percent:
            print("CRITICAL: Memory Low - Current Free: %s%%  Threshold:%s%%") % \
                (int(_freemem_percent), _args.critical)
            exit(2)
        elif _args.warning and _args.warning > _freemem_percent:
            print("WARNING: Memory Low - Current Free: %s%%  Threshold:%s%%") % \
                (int(_freemem_percent), _args.warning)
            exit(1)
    else:
        _used_percent = (used / total) * 100
        if _args.critical and _args.critical < _used_percent:
            print("CRITICAL: Memory Low - Current Used: %s%%  Threshold:%s%%") % \
                (int(_used_percent), _args.critical)
            exit(2)
        elif _args.warning and _args.warning < _used_percent:
            print("WARNING: Memory Low - Current Used: %s%%  Threshold:%s%%") % \
                (int(_used_percent), _args.warning)
            exit(1)


def print_help(parser):
    parser.print_help()
    exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Disk Filesystem Usage")
    parser.add_argument('-c', '--critical',
                        type=int,
                        metavar='PERCENT',
                        default=95,
                        help='Percent Filesystem Usage Critical Threshold')
    parser.add_argument('-w', '--warning',
                        type=int,
                        metavar='PERCENT',
                        default=90,
                        help='Percent Filesystem Usage Warning Threshold')
    parser.add_argument('--used', dest='free', action='store_false',
                        default=False,
                        help='Calculate Threshold using Used RAM')
    parser.add_argument('--free', dest='free', action='store_true',
                        help='Calculate Threshold based on Free RAM')

    _args = parser.parse_args()
    check_memory(_args)
