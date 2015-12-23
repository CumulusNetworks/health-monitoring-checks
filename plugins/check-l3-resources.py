#!/usr/bin/env python
"""
 This filename contains a health monitoring plugin which is still
 being developed and is still in the alpha testing stage.
 ----------------------------------------------------------------

 check-l3-resources

 DESCRIPTION

 OUTPUT
    plain text

 PLATFORMS:
    Cumulus Linux Hardware Switch Only

 DEPENDENCIES:
    Python 2.7+

 USAGE:
   check-l3-resources -w 90 -c 99

 ARGUMENTS:
   --warning: warning if any L3 Cumulus resource is greater than set threshold.
              Default is 95%
   --critical: send critical exit code if any L3 Cumulus resouce is greater than
               set threshold. Default is 95%
   -w: alias to --warning
   -c: alias to --critical

 NOTES:
   This check supports checking all l3 resources mentioned in cl-resources-query
   except Egress ACL slices(which is always at 100%)

   Cannot be tested on Cumulus VX.

 TODO:

 LICENSE:
   Copyright 2015 Cumulus Networks
   Original Author: Stanley Karunditu <stanleyk@cumulusnetworks.com>
   Released under the the MIT license. see LICENSE for details.
"""

import argparse
import subprocess


def check_l3_resources(_args):
    try:
        cmd = '/usr/cumulus/bin/cl-resource-query -k'.split()
        out = subprocess.check_output(cmd)
    except OSError as e:
        print("problem executing cl-resource-query %s " % (e))
        exit(2)

    _output = out.splitlines()
    l3_resources_to_check = convert_data_to_dict(_output)
    for _key, _entry in l3_resources_to_check.items():
        _max = _entry.get('max')
        _count = _entry.get('count')
        if not _max or not _count or _key == 'eg_acl_slice':
            continue
        percent_diff = (float(_count) / float(_max)) * 100
        if _args.critical and percent_diff > _args.critical:
            print("CRITICAL: %s L3 Resource " % (_key) +
                  "Current: %s Max: %s Threshold: %s%%" %
                  (_count, _max, _args.critical))
            exit(2)
        elif _args.warning and percent_diff > _args.warning:
            print("WARNING: %s L3 Resource " % (_key) +
                  "Current: %s Max: %s Threshold: %s%%" %
                  (_count, _max, _args.warning))
            exit(1)


def convert_data_to_dict(_output):
    # Opened bug to have cl-resource-query output in JSON. Then this function
    # is not needed
    l3_resources_to_check = {}
    for _line in _output:
        (_fullname, _value) = _line.split('=')
        _fullname_arr = _fullname.split('_')
        _max_or_count = _fullname_arr.pop(-1)
        _prefix = '_'.join(_fullname_arr)
        if _prefix not in l3_resources_to_check:
            l3_resources_to_check[_prefix] = {}

        l3_resources_to_check[_prefix][_max_or_count] = int(_value)

    return l3_resources_to_check


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check Cumulus L3 Resources. " +
        "Found in cl-resource-query output")
    parser.add_argument('-w', '--warning',
                        type=int,
                        default=90,
                        metavar='PERCENT',
                        help='Percent used after which warning exit code is issued')
    parser.add_argument('-c', '--critical',
                        type=int,
                        default=95,
                        metavar='PERCENT',
                        help='Percent used after which critical exit code is issued')

    _args = parser.parse_args()
    check_l3_resources(_args)
