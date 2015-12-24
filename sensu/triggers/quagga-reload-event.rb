#! /usr/bin/env ruby
#
#  This file  contains Health monitoring plugins or checks definitions
#  which are still being developed and are still in the alpha testing stage
#  ------------------------------
#
# quagga-reload-event
#
# DESCRIPTION:
#
#  Sends a Quagga Routing Protocol Reload Sensu Event to the local Sensu Client.
#  Sends it as a critical alert - status == 2
#
# OUTPUT
#   plain text
#
# PLATFORMS
#   Linux
#   Cumulus Linux Quagga (may work with regular Quagga)
#
# DEPENDENCIES
#    ruby
#    gem socket
#    gem json
#    gem optparse
#    gem ostruct
#
# ARGUMENTS
#   Feed it ${watchquagga_options[@]} from the /etc/init.d/quagga bash script
#   The handler option below is required.
#   --handler: Provide an array of handlers that will manage this critical alert
#
#
# USAGE:
#
#
#   tells the script to trigger a critical alert and send the message to
#   pagerduty and email handler
#
#    /etc/sensu/plugins/quagga-reload-event.rb --handler pagerduty,email "${watchquagga_options[@]}"
#
#  ```
#
# NOTES:
#  ${watchquagga_options[@] options are as follows
#  Option: -adz
#  Option: -r /usr/sbin/servicebBquaggabBrestartbB%s
#  Option: -s /usr/sbin/servicebBquaggabBstartbB%s
#  Option: -k  /usr/sbin/servicebBquaggabBstopbB%s
#  Option: -b  bB
#  Option: -t 30
#  Argument: zebra
#  Argument: bgpd
#
#  This script using Optparse, scripts the ARGV array of all Options and leaves
#  only the 2 arguments, the routing protocols that were reset. It takes those
#  routing protocol names and crafts a useful critical messgae informing the
#  user of exactly which service was restarted
#
#  This script is to be placed in /etc/init.d/quagga start(), right under the
#  start-stop-daemon call. This is because watchquagga doesn't
#  support a way to trigger a script when it reloads a service. A bug has been
#  filed to address this in watchquagga.
#
#   Embed the trigger in the start() function /etc/init.d/quagga bash script. Like
#   this
#   ```
#  # Starts the server if it's not alrady running according to the pid file.
#  The Quagga daemons creates the pidfile when starting.
#  start()
#  {
#  if [ "$1" = "watchquagga" ]; then
#
#    # We may need to restart watchquagga if new daemons are added and/or
#    # removed
#    if started "$1" ; then
#      stop watchquagga
#    else
#      # Echo only once. watchquagga is printed in the stop above
#      echo -n " $1"
#    fi
#
#
#    start-stop-daemon \
#      --start \
#      --pidfile=`pidfile $1` \
#      --exec "$D_PATH/$1" \
#      -- \
#      "${watchquagga_options[@]}"
#    ### SENSU TRIGGER
#    /etc/sensu/plugins/quagga-reload-event.rb --handler pagerduty,logstash "${watchquagga_options[@]}"
#    ###
#
#   ```
#
#
# TODO:
# LICENSE:
#    Copyright 2015 Cumulus Networks
#    Original Author: Stanley Karunditu <stanleyk@cumulusnetworks.com>
#    Released under the the MIT license. see LICENSE for details.
#
require 'json'
require 'socket'
require 'optparse'
require 'ostruct'


def send_event(metric_name, options, msg, check_type='standard')
  data = {
    'name'      => metric_name,
    'type'      => check_type,
    'output'    => msg,
    'handlers'  => options.handler,
    'status'    => 2
  }
  # Dump the data to the socket
  socket = TCPSocket.new '127.0.0.1', 3030
  socket.print data.to_json
  socket.close
end

options = OpenStruct.new
OptionParser.new do |opts|
  opts.banner = "Trigger Sensu Event when Quagga Restarts a Routing Protocol"
  opts.separator ""
  opts.on('-a') {  options.a_flag = true }
  opts.on('-d') {  options.d_flag = true }
  opts.on('-z') {  options.z_flag = true }
  opts.on("-s <SOMETHING>") { |val| options.s_flag = val }
  opts.on("-r <SOMETHING>") { |val| options.r_flag = val }
  opts.on("-k <SOMETHING>") { |val| options.k_flag = val }
  opts.on("-b <SOMETHING]") { |val| options.b_flag = val }
  opts.on("-t <SOMETHING>") { |val| options.t_flag = val }
  opts.on("--handler <HANDLER1,HANDLER2>", "List Sensu Handlers to use in triggered alert", String) do |val|
    options.handler = val.split(',')
  end
  opts.on_tail("-h", "--help", "Show this message") do
    p "Script of Triggering Sensu Event when Quagga reloads"
    p "Read the Script header for more details on usage"
    exit
  end
end.parse!
reloaded_services = ARGV
msg = "WatchQuagga has restarted #{reloaded_services.join(" ")} protocols"
metric_name = 'quagga_routing_protocol_restart'
if ARGV.length > 0
  send_event(metric_name, options, msg)
end
