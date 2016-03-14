# Suggestions for Sensu Check Examples

This folder contains sensu check definition files (.json) files
that provide suggestions on how to use the checks in the ``plugin``
folder on the Sensu Health Monitoring Platform.

All checks are defined as standalone checks. This provides the
flexibility to adjust the interval, refresh and occurrence rates
on a per platform basis. A configuration management tool
like Ansible or Puppet can easily manage this.

When a change is made, only the sensu-client on the affected host needs
to be restarted.

## Routing Checks

### check-bgp-peers.json
The suggested interval to check bgp peer status is 30 seconds


### check-bgp-routes.json
The suggested check interval is 30 seconds.
Some users may have requirements that a minimum number of
bgp routes must be seen on every switch as a way to verify
that routing is working. This could be some external routes
advertised by an external AS.

## Environmental Checks

### check-cumulus-fans.json
Suggested check interval is 60 seconds. By default it produces a warning
message if the fan speed is 90% of the max and a critical message if 95%
of the max fan speed

### check-cumulus-psu.json
Suggested check interval is 60 seconds. Requires a user to define
how many PSUs can run without generating a critical alert.

### check-cumulus-temp.json
Suggested check interval is 60 seconds. `smonctl` the environmental management
interface for Cumulus Linux provides critical and warning thresholds for all
temperature sensors. This check will execute if the temperature is within 2%
of either a warning or critical threshold.

## System Checks

### check-cpu.json
The suggested check interval is 30 seconds with the event handler kicking
in if there are 3 occurrences in 5 minutes. This way if BGP or Switchd cause
a temporary spike in the CPU, no event will be triggered

### check-disk.json
The suggested check interval is 60 seconds. Disk usage on a Cumulus switch
should not vary much.

### check-memory.json
The suggested check interval is 60 seconds

### check-process-bgp.json
The suggested interval is 60 seconds. This check should
never be triggered. It can only happen if jdoo is down, and watchquagga
is down and BGP crashes. A very rare event. But because BGP is a critical
process to the running of the switch its important to run this check.
A possibility here is to include a dependency check to only run this
check if the watchquagga check fails.

### check-process-jdoo.json
Suggested check interval is 60 seconds.
Jdoo in Cumulus 2.5.X is responsible for maintaining the process state of
``switchd``, ``switchd`` and ``watchquagga``. It is important this process
is never down. It should be a very rare occurrence.

### check-process-switchd.json
Suggested check interval is 60 seconds
Switchd is probably the most critical process on the Cumulus Linux platform.
It is kept up, using Jdoo (Cumulus 2.5.X) and monitoring it to ensure
that it is not never down is important. It should be a very rare occurrence

### check-process-watchquagga.json
Suggested check interval is 60 seconds
Watchquagga is responsible for maintaining the routing protocol processes.
It should never be down. Jdoo in Cumulus 2.5.X is responsible for keeping it
up but monitoring this process to ensure that it is not down is important.
This check should rarely if ever fire. A possibility here is to include a
dependency check where this definition only executes if the jdoo check fails.
