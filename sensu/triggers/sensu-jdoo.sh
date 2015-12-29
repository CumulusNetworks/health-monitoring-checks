#!/bin/bash

# sensu-jdoo.sh
#
# DESCRIPTION
#  Simple BASH Script for sending triggered alerts from Jdoo to a Sensu Server
#
# OUTPUT
#   plain text
#
# PLATFORMS:
#   Linux
#   Jdoo
#
# DEPENDENCIES:
#   Bash
#
# USAGE:
#  sensu-jdoo.sh
#
# LICENSE:
#   Copyright: Cumulus Networks
#   Author: Stanley Karunditu <stanleyk@cumulusnetworks.com>
#   Derived from Documentation found in
#   https://sensuapp.org/docs/0.21/clients#client-socket-input
#   Released under the terms of the MIT License. See LICENSE for more details
#
# NOTES
#
# Copy the sensu-jdoo.sh script to a reasonable location. A suggested location
# is /etc/sensu/triggers. Ensure the script is executable by the sensu user
#
# Modify the sensu-jdoo.sh script variables to suit your needs.
#
# Modify jdoo file with a statement at the end of the monit check that 
# says on restart, trigger the sensu event. Below is an example.
# 
# ```
# check process lldpd with pidfile /var/run/lldpd.pid
#        every 2 cycles
#        group networking
#        start program = "/etc/init.d/lldpd start"
#        stop program = "/etc/init.d/lldpd stop"
#        if does not exist then restart else if succeeded then exec "/etc/sensu/triggers/sensu-jdoo.sh"
#
# ```
#
# Restart Jdoo
#
#
# The remaining portion of the notes discusses how to test this trigger script.
# It uses the LLDP process restart check example shown above. 
# To test the trigger, start a tail log that looks for any jdoo events
# ```
# $ sudo tail -f /var/log/syslog | grep jdoo &
# ```
#
# Check that the process exists
# ```
# $ pgrep lldpd
# 29490
# 29492
# ```
#
# Pkill the process
# ```
# $ sudo pkill lldpd
# ```
#
# Pgrep the process to ensure it is died. 
# ```
# $ sudo pgrep lldpd
# ```
#
# Wait for a message to show up on the terminal from the tail log
# ```
# 2015-12-29T03:48:19.595216+00:00 s4048-2 jdoo[28272]: 'lldpd' process is not running
# 2015-12-29T03:48:19.595250+00:00 s4048-2 jdoo[28272]: 'lldpd' trying to restart
# 2015-12-29T03:48:19.595536+00:00 s4048-2 jdoo[28272]: 'lldpd' start: /etc/init.d/lldpd
# 2015-12-29T03:49:20.641661+00:00 s4048-2 jdoo[28272]: 'lldpd' process is running with pid 29490
# 2015-12-29T03:49:20.641695+00:00 s4048-2 jdoo[28272]: 'lldpd' exec: /etc/sensu/triggers/sensu-jdoo.sh
# 2015-12-29T03:49:23.686090+00:00 s4048-2 sensu: {"timestamp":"2015-12-29T03:49:20.647801+0000","level":"info","message":"publishing check # result","payload":{"client":"s4048_2","check":{"name":"jdoo_restart_process","output":"lldpd was reset by Jdoo","status":2,"handlers":# #3
# ["pagerduty","email"],"executed":1451360960,"issued":1451360960}}}
#
# ```
########################################################


##### Modify the following variables ############

# $MONIT_SERVICE is passed from Jdoo into this script
# see manpage for jdoo for more details on Shell variables
# passed from Jdoo into trigger scripts like this one
OUTPUT="${MONIT_SERVICE} was reset by Jdoo"

# critical status(2),  warning status (1)
STATUS=2

HANDLER_LIST='"pagerduty", "email"'

########################


SENSU_CHECK="{ \"name\": \"jdoo_restart_process\", \"output\": \"${OUTPUT}\",
\"status\": ${STATUS}, \"handlers\": [$HANDLER_LIST]}"

# for debugging uncomment this line
# echo $SENSU_CHECK

echo ${SENSU_CHECK} > /dev/tcp/localhost/3030

