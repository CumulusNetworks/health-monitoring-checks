#! /usr/bin/env ruby
#  encoding: UTF-8
#
#   routing protocol statistics
#
# DESCRIPTION:
#   Returns Routing protocol neighbor count and total route count.
#   This can be applied to a time series graph to check for major fluctuations.
#   If major fluctations occur with these route counts, then it is a sign that
#   something is wrong with the switch. Specifically written to work on Cumulus
#   Linux. Makes use the non-modal CLI created by Cumulus Linux
#
# OUTPUT:
#   Generates 2 events.
#   1. routes_stats metric event. Output
#      - list of routes
#      - total route count learned from that routing protocol
#   2. peer_stats metric event. Output:
#      - total peer count
#      - list of peer IPs in a working state (currently only supports BGP)
#      - peer  working state count
#      - list of peers not in a working state (currently works only for BGP)
#      - peer not working state count
#
#
# PLATFORMS:
#   Linux
#
# DEPENDENCIES:
#   gem: sensu-plugin
#   gem: socket
#   gem: json
#
# USAGE:
#   /etc/sensu/plugins/metrics/metrics-router-stats.rb -h logstash
#
# NOTES:
#
# LICENSE:
#
# Copyright 2015 Cumulus Networks, Inc. All rights reserved.
# Author: Stanley Karunditu <stanleyk@cumulusnetworks.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.
# 51 Franklin Street, Fifth Floor
# Boston, MA  02110-1301, USA.
#

require 'sensu-plugin/metric/cli'
require 'json'
require 'socket'

class RoutingProtocolStats < Sensu::Plugin::Metric::CLI::JSON
  option :route_protocol,
         description: 'What type of routing protocol. Right now only supports "bgp"',
         short: '-r ROUTE_PROTOCOL',
         long: '--routing-protocol ROUTE_PROTOCOL',
         default: "bgp"

  option :handler,
         description: 'The handler(s) to use for the route and peer metrics.',
         short: '-h HANDLER[,HANDLER]',
         long: '--handler HANDLER[,HANDLER]',
         default: 'logstash',
         proc: proc { |a| a.split(',') }

  # Need to amend the sensu-plugin metric with a send event option. Perhaps
  # even upstream it
  def send_event(metric_name, output, check_type='metric')
    data = {
      'name'      => metric_name,
      'type'      => check_type,
      'output'    => output,
      # Convert to an array here explicilty incase a single handler is given
      'handlers'  => config[:handler], #Array(config[:handler]),
      'status'    => 0
    }
    # Dump the data to the socket
    socket = TCPSocket.new '127.0.0.1', 3030
    socket.print data.to_json
    socket.close
  end

  # this cmd_to_run should work with both OSPF and BGP. Testing only with BGP
  # ipv4.
  def send_route_stats
    cmd_to_run = "cl-#{config[:route_protocol]} route show json"
    json_output = JSON.parse(IO.popen(cmd_to_run).read())
    routes = json_output.fetch('routes').keys()
    output = {
      'routes' => routes,
      'route_count' => routes.length
    }.to_json
    send_event('route_stats', output)
  end


  # Only works with BGP ipv4 right now
  def send_neighbor_stats
    cmd_to_run = "cl-#{config[:route_protocol]} summary show json"
    json_output = JSON.parse(IO.popen(cmd_to_run).read())
    neighbors = json_output.fetch('peers')
    peers_working = []
    peers_failed_state = []
    # Currently tests for BGP only
    neighbors.each do | _peer, _peerstats |
      if _peerstats.fetch('state').eql? 'Established'
        peers_working.push(_peer)
      else
        peers_failed_state.push(_peer)
      end
    end
    output = {
      'total_peer_count' => json_output.fetch('total-peers'),
      'peers_working' => peers_working,
      'peers_working_count' => peers_working.count,
      'peers_failed_state' => peers_failed_state,
      'peers_failed_state_count' => peers_failed_state.count
    }.to_json
    send_event('peer_stats', output)
  end

  def run
    send_route_stats
    send_neighbor_stats
    ok
  end
end
