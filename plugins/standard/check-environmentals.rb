#! /usr/bin/env ruby
#  encoding: UTF-8
#
#   check-environmentals
#
# DESCRIPTION:
#   Send a Warning message if an environmental sensor is
#   more than the warning threshold.
#   Send a critical message if sensor is beyond critical threshold.
#   Send an event if minimum number of working fans is
#   less than --min-fans or --min-psu
#   Multiple events can be generated from this check
#
# OUTPUT:
#   plain text
#
# PLATFORMS:
#   Cumulus Linux
#
# DEPENDENCIES:
#   gem: sensu-plugin
#        socket
#        json
#
# USAGE:
#  Set warning threshold to 85% and critical threshold to 97%
#  So if the max Fan speed is 12000 RPM and current fan speed is 11900 RPM
#  a critical event is sent because current fan speed is
#  greater than 97% of max recommended fan speed.
#  Minimum number of fans working is 2. anything lower i
#  and an alert is issued.
#   ./check-environmentals.rb -w 85 -c 97 --min-fans 2 --min-psu 2 --handler "email"
#
#
# NOTES:
#
# LICENSE:
#   Copyright 2015 Cumulus Networks
#   Released under the same terms as Sensu (the MIT license); see LICENSE
#   for details.
#
require 'rubygems' if RUBY_VERSION < '1.9.0'
require 'sensu-plugin/check/cli'
require 'socket'
require 'json'

class CheckEnvironmentals < Sensu::Plugin::Check::CLI
  option :warn,
         short: '-w WARN',
         proc: proc(&:to_i),
         default: 90

  option :crit,
         short: '-c CRIT',
         proc: proc(&:to_i),
         default: 95
  option :min_fans,
         short: '-f COUNT',
         long: '--min-fans',
         proc: proc(&:to_i),
         default: 2
  option :min_psu,
         short: '-f COUNT',
         long: '--min-psu',
         proc: proc(&:to_i),
         default: 2

  option :handler,
         short: '-h HANDLER',
         long: '--handler',
         default: "debug"

  def send_event(metric_name, output, status, check_type='check')
    data = {
      'name'      => metric_name,
      'type'      => check_type,
      'output'    => output,
      # Convert to an array here explicilty incase a single handler is given
      'handlers'  => config[:handler], #Array(config[:handler]),
      'status'    => status
    }
    puts data.to_json

    # Dump the data to the socket
    #socket = TCPSocket.new '127.0.0.1', 3030
    #socket.print data.to_json
    #socket.close
  end


  def check_fan
    check_name = 'check_fan'
    fan_count = 0

    @smonctl.each do |sensor|
      if sensor.fetch('type').eql? 'fan'
        if sensor.fetch('state').eql? 'OK'
          if not sensor.fetch('name').start_with?("PSU") and
            fan_count += 1
          end
          max = sensor.fetch('max')
          curr = sensor.fetch('input')
          percent_diff = (curr/max)  * 100
          if percent_diff > config[:warn]
            msg = "WARNING: #{sensor.fetch('description')} "  +
            "Current: #{curr}  Max: #{max} Threshold: #{config[:warn]}%"
            send_event(check_name, msg, 1)
          elsif percent_diff > config[:crit]
            msg = "CRITICAL: #{sensor.fetch('description')} " +
            "Current: #{curr} Max: #{max} Threshold:#{config[:warn]}%"
            send_event(check_name, msg, 2)
          end
        end
      end
    end
    if fan_count < config[:min_fans]
      msg = "CRITICAL: Fan Count Low: #{fan_count} Threshold:#{config[:min_fans]}"
      send_event(check_name, msg, 2)
    end
  end

  def check_temp
    check_name = 'check_temp'
    @smonctl.each do |sensor|
      if sensor.fetch('type').eql? 'temp'
        if sensor.fetch('state').eql? 'OK'
          max = sensor.fetch('max')
          curr = sensor.fetch('input')
          percent_diff = (curr/max) * 100
          puts "max #{max} curr #{curr} percent_diff #{percent_diff}"
          if percent_diff > config[:warn]
            msg = "WARNING: #{sensor.fetch('description')} "  +
            "Current: #{curr} Max: #{max} Threshold: #{config[:warn]}%"
            send_event(check_name, msg, 1)
          elsif percent_diff > config[:crit]
            msg = "CRITICAL: #{sensor.fetch('description')} " +
            "Current: #{curr} Max: #{max} Threshold:#{config[:warn]}%"
            send_event(check_name, msg, 2)
          end
        end
      end
    end
  end


  def check_psu
    psu_count = 0
    check_name = 'check_psu'
    @smonctl.each do |sensor|
      if sensor.fetch('type').eql? 'power'
        if sensor.fetch('state').eql? 'OK'
          psu_count += 1
        end
      end
    end
    if psu_count < config[:min_psu]
      msg = "CRITICAL: Power Supply Count Low Threshold: #{config[:min_psu]}"
      send_event(check_name, msg, 2)
    end
  end

  def run
    @smonctl = JSON.parse(IO.popen('smonctl -j').read)
    check_fan
    check_temp
    check_psu
    ok
  end
end

