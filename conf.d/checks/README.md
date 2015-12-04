# Notes on each check
According to the creator of JSON, JSON should have no comments. No moved all the
comments out of the JSON files into this README.

##check-process-bgp.json

This is an example of checking the bgp process state. This check only activates if watchquagga process is died and jdoo(monit-like program) fails to restart watchquagga. This check should rarely if ever be activated. This check only sends critical sensu events. Only run this check if bgp is activated in the /etc/quagga/daemons file

##check-cpu.json

This is an example standard check that executes the plugin check-cpu.rb. it
sets the default critical threshold at 99% with a warning alert issued at 95%
the check is triggered only if 3 occurrences happen within 10 minutes.
Then every 10 minutes, if 3 occurrences happen again, another alert is
triggered. The default handler is to send the event to logstash.

##check-disk.json
This is an example standard check that executes the plugin check-disk.rb. it sets the default critical threshold at 95% on any partition and/or total disk space used the check is triggered only if 1 occurrence happens within 30 minutes

##check-memory.json
This is an example standard check that executes the plugin check-memory.rb. it sets the default critical threshold at 95% and a
warn threshold on 85%. The check is triggered only if 3 occurrences happens within 10 minutes when the check is triggered a copy of the event is sent to logstash for further processing and storage in a datastore.

## check-process-ntp.json
This is a an example standard check that observes the process table and sends a critical alert if the ntp process goes down. This is important to the working of CLAG and monitoring.

## check-process-switchd.json
This is a critical program to the working of the switch. This process should
never go down. Jdoo (monit like program) should ensure that it never stays down
for long.

##check-process-watchquagga.json
This is an example of checking the watchquagga process state. This check only activates if watchquagga process is died and jdoo(monit-like program) fails to restart watchquagga. This check should rarely if ever be activated.
This check only sends critical sensu events. Process check occurs every 10 seconds and activates if watchquagga is done once in an 1800 sec interval.

## LICENSE:
   Copyright 2011 Sonian, Inc <chefs@sonian.net>
   Copyright 2015 Cumulus Networks <ce-ceng@cumulusnetworks.com>
   Released under the same terms as Sensu (the MIT license); see LICENSE for details.
