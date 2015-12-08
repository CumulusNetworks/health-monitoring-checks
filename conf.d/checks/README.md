# Notes on each check
According to the creator of JSON, JSON should have no comments. No moved all the
comments out of the JSON files into this README.

## client.json.example
Example of client.json file. Shows how to set the thresholds as well as how to
set the handler when the keepalive between client/server fails.

##check-bgp-peers.json
Checks how many non-established BGP peers are present on
a switch. The default is to send a critical alert when a non-established BGP
peer is detected. This check only executes if the `check-process-bgp` check
succeeds

## check-bgp-routes.json
Checks how many routes are learned from BGP. A critical event is issued if the
number of BGP routes is less than the minimum defined. The minimum defined is 1.
There should be at least 1 BGP route in the table.

##check-process-bgp.json

Checks the bgp process state. This check only activates if watchquagga process is died and jdoo(monit-like program) fails to restart watchquagga. This check should rarely if ever be activated. This check only sends critical sensu events. Only run this check if bgp is activated in the /etc/quagga/daemons file

##check-cpu.json

Standard check that executes the plugin check-cpu.rb. it
sets the default critical threshold at 99% with a warning alert issued at 95%
the check is triggered only if 3 occurrences happen within 10 minutes.
Then every 10 minutes, if 3 occurrences happen again, another alert is
triggered. The default handler is to send the event to logstash.

##check-disk.json
Standard check that executes the plugin check-disk.rb. it sets the default critical threshold at 95% on any partition and/or total disk space used the check is triggered only if 1 occurrence happens within 30 minutes

##check-memory.json
Standard check that executes the plugin check-memory.rb. it sets the default critical threshold at 95% and a
warn threshold on 85%. The check is triggered only if 3 occurrences happens within 10 minutes when the check is triggered a copy of the event is sent to logstash for further processing and storage in a datastore.

## check-process-ntp.json
Standard check that observes the process table and sends a critical alert if the ntp process goes down. This is important to the working of CLAG and monitoring.

## check-process-switchd.json
Checks that switchd never stays down. This is a critical program to the working of the switch. This process should
never go down. Jdoo (monit like program) should ensure that it never stays down
for long.

##check-process-watchquagga.json
Checks the watchquagga process state. This check only activates if watchquagga process is died and jdoo(monit-like program) fails to restart watchquagga. This check should rarely if ever be activated.
This check only sends critical sensu events. Process check occurs every 10 seconds and activates if watchquagga is done once in an 1800 sec interval.


## bgp-route-peer-metrics.json
Collects route and peer metrics from BGP.
