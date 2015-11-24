#! /usr/bin/env ruby
#  encoding: UTF-8
#
#   interface-metrics
#
# DESCRIPTION:
#
# OUTPUT:
#   metric data
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
#
# NOTES:
#
# LICENSE:
#

require 'sensu-plugin/metric/cli'
require 'json'
require 'socket'

class InterfaceGraphite < Sensu::Plugin::Metric::CLI::JSON
  option :scheme,
         description: 'Metric naming scheme, text to prepend to metric',
         short: '-s SCHEME',
         long: '--scheme SCHEME',
         default: "#{Socket.gethostname}.interface"

  def send_single_iface_event(_iface, _value)
    data = {
      'name'      => 'single_iface_counters',
      'type'      => 'metric',

      # Convert to an array here explicilty incase a single handler is given
      'handlers'  => ['logstash'], #Array(config[:handler]),
      'status'    => 0
    }

    # construct iface_event json
    iface_event = {
      'iface_name' => _iface,
      'total_tx'  => _value['iface_obj']['counters']['total_tx'],
      'total_rx'  => _value['iface_obj']['counters']['total_rx'],
      'total_err' => _value['iface_obj']['counters']['total_err']
    }.to_json
    data['output'] = iface_event
    # Dump the data to the socket
    socket = TCPSocket.new '127.0.0.1', 3030
    socket.print data.to_json
    socket.close
  end


  def run
    json_output = JSON.parse(IO.popen("netshow counters -j").read())

    json_output.each do |_iface, _value|
      send_single_iface_event(_iface, _value)
    end
    ok
  end
end
