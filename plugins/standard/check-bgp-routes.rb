#! /usr/bin/env ruby
#  encoding: UTF-8
#
#   Check bgp route count in Quagga
#
# DESCRIPTION:
#   Returns a critical message when the number of BGP routes dips below a
#   specified number. Run the check.json for this plugin with a dependency
#   on check-process for bgpd.
#
# PLATFORMS:
#   Linux
#
# DEPENDENCIES:
#   gem: sensu-plugin
#   quagga
#
# USAGE:
#   check-bgp-routes.rb --min-routes 0
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

class CheckBGPRoutes < Sensu::Plugin::Check::CLI
  option :min_routes,
    description: "Minimum routes in BGP table before sending a critical event",
    long: "--min-routes MIN_ROUTES_CRIT",
    default: 0

  def run
    cmd_to_run = "cl-bgp route show json"
    json_output = JSON.parse(IO.popen(cmd_to_run).read())
    routes = json_output.fetch('routes').keys()
    if routes.length <= config[:min_routes].to_i
      critical "Number of BGP Routes Too Low - #{routes.length} "
    end
    ok
  end
end
