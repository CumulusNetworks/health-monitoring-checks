#!/usr/bin/env python
"""
For SE Monitoring Demo. Converts Non Established Peer Count into a metric
This is then consumed by telegraf input exec plugin
This file for demo purposes only
This file is placed in /usr/local/bin/bgp_stats_influxdb.py
LICENSE: MIT
Author: Stanley Karunditu
Copyright: Cumulus Networks
"""
import json
import subprocess


def parse_bgp_output():
    """
    Parse BGP JSON Output
    :return: JSON string with BGP Peer info
    """
    json_str = ''
    try:
        cmd = ["/usr/bin/sudo", "/usr/bin/vtysh", "-c", 'show ip bgp sum json']
        json_str = subprocess.check_output(cmd)
    except OSError as e:
        print("problem executing vtysh %s " % (e))
        exit(2)
    return json_str


def stream_bgp_metrics():
    """
    Get BGP JSON Output. Massage it a little to generate
    metrics for non-established peers. Print output as
    JSON for telegraf consumption.
    """
    bgp_output = parse_bgp_output()
    parsed_json = json.loads(bgp_output)
    neighbors = parsed_json.get('peers')
    final_json = dict()
    failedPeers = 0
    for _peer, _peerstats in neighbors.items():
        if _peerstats.get('state') != 'Established':
            failedPeers += 1
    final_json['totalPeers'] = parsed_json.get('totalPeers')
    final_json['failedPeers'] = failedPeers
    return json.dumps(final_json)

if __name__ == "__main__":
    print stream_bgp_metrics()