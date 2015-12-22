#!/usr/bin/env python
"""
 This filename contains a health monitoring plugin which is still
 being developed and is still in the alpha testing stage.
 ----------------------------------------------------------------

 check-disk

 DESCRIPTION
   Check Disk Usage by filesystem, by analysing the output from the "df -x tmpfs" command.

 OUTPUT
    plain text

 PLATFORMS:
    Linux

 DEPENDENCIES:
    Python 2.7+

 USAGE:
   check-disk.py -w 80 -c 90

 ARGUMENTS:
   --warning:  Percent fileystem usage beyond which an exit code of 1 is returned
   -w: alias for --warning
   --critical: Percent filesystem usage beyond which an exit code of 2 is returned
   -c: alias for --critical

 NOTES:
   After researching several nagios disk checks, found it very complicated. This
   is a simple version useful for network switches - Stanley K.

 TODO:

 LICENSE:
   Copyright 2015 Cumulus Networks
   Original Author: Stanley Karunditu <stanleyk@cumulusnetworks.com>
   Released under the the MIT license. see LICENSE for details.
"""

import argparse
import sys
import subprocess


def check_disk(_args):
    cmd = '/bin/df -x tmpfs'
    df_output = None
    try:
        df_output = subprocess.check_output(cmd.split())
    except IOError as e:
        print("failed to execute df %s" % (e))
        exit(2)
    for _entry in df_output.split('\n'):
        _entry_details = _entry.split()
        _filesystem = None
        _percent_used = None
        _msg = None
        _code = 0
        if len(_entry_details) > 0 and _entry_details[0] == 'Filesystem':
            continue
        try:
            _filesystem = _entry_details[-1]
            _percent_used = int(_entry_details[-2].split('%')[0])
        except ValueError and IndexError:
            continue
        if _percent_used and _args.critical and _percent_used > _args.critical:
            _msg = "CRITICAL: Filesystem '%s' Usage Passed Threshold " % (_filesystem) + \
                "Current:%s%%  Threshold:%s%%" % (_percent_used, _args.critical)
            _code = 2
        elif _percent_used and _args.warning and _percent_used > _args.warning:
            _msg = "WARNING: Filesystem '%s' Usage Passed Threshold " % (_filesystem) + \
                "Current:%s%%  Threshold:%s%%" % (_percent_used, _args.warning)
            _code = 1

        if _msg:
            print(_msg)
            exit(_code)


def print_help(parser):
    parser.print_help()
    exit(2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Disk Filesystem Usage")
    parser.add_argument('-c', '--critical',
                        type=int,
                        metavar='PERCENT',
                        help='Percent Filesystem Usage Critical Threshold')
    parser.add_argument('-w', '--warning',
                        type=int,
                        metavar='PERCENT',
                        help='Percent Filesystem Usage Warning Threshold')

    if (len(sys.argv) < 2):
        print_help(parser)

    _args = parser.parse_args()
    check_disk(_args)
