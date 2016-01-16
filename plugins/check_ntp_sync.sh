#!/bin/sh
#
# michaszek@o2.pl
# Checks if the ntp service synchronises to the server time, gives ntp server IP and offset.
# Tested on Ubuntu 12.04.
# From Nagios Exchange
# https://exchange.nagios.org/directory/Plugins/Network-Protocols/NTP-and-Time/check_ntp_server_sync/details
# LICENSE GPL
COMMAND=$(ntpq -pn | grep -F '*' | awk '{print $1}' | cut -d "*" -f 2)
OFFSET=$(ntpq -pn | grep -F '*' | awk '{print $9}')

if [ -z "$COMMAND" ]
then
        echo "No synchronization with the time server"
        exit 2

else
        echo "Synchronized with the server: "$COMMAND" offset: "$OFFSET
        exit 0
fi
