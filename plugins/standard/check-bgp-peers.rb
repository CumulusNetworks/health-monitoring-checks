#! /usr/bin/env ruby
#  encoding: UTF-8
#
#   Check bgp peer status
#
# DESCRIPTION:
#   Returns a critical message  BGP reports a number of BGP peers that are
#   not in an established state
#
# PLATFORMS:
#   Linux
#
# DEPENDENCIES:
#   gem: sensu-plugin
#   quagga
#
# USAGE:
#   check-bgp-peers.rb --min-down-peers 2
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
require 'sensu-plugin/check/cli'
require 'json'

class CheckBGPPeers < Sensu::Plugin::Check::CLI
  option :min_down_peers,
    description: "Minimum Non-Established BGP Peer Count",
    long: "--min-down-peers MIN_PEERS_CRIT",
    default: 1

  def run
    cmd_to_run = "cl-bgp summary show json"
    json_output = JSON.parse(IO.popen(cmd_to_run).read())
    neighbors = json_output.fetch('peers')
    peers_not_working_count = 0
    neighbors.each do | _peer, _peerstats |
      if _peerstats.fetch('state') != 'Established'
        peers_not_working_count += 1
      end
    end
    if peers_not_working_count >= config[:min_down_peers].to_i
      critical "Number of Non Established BGP Peers - #{peers_not_working_count} "
    end
    ok
  end
end
