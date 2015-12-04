#! /usr/bin/env ruby
#  encoding: UTF-8
#
#   mermory-usage-metrics
#
# DESCRIPTION:
#
# OUTPUT:
#   JSON metric data
#
# PLATFORMS:
#   Linux
#
# DEPENDENCIES:
#   gem: sensu-plugin
#   gem: socket
#
# USAGE:
#
# NOTES:
#  - Original file
#  https://raw.githubusercontent.com/sensu/sensu-community-plugins/master/plugins/system/memory-metrics-percent.rb
#  - Modified by Stanley Karunditu <stanleyk@cumulusnetworks.com> to output
#  JSON. Renamed to memory-usage-metrics
#
# LICENSE:
#   Copyright 2012 Sonian, Inc <chefs@sonian.net>
#   Released under the same terms as Sensu (the MIT license); see LICENSE
#   for details.
#

require 'rubygems' if RUBY_VERSION < '1.9.0'
require 'sensu-plugin/metric/cli'
require 'socket'

class MemoryGraphite < Sensu::Plugin::Metric::CLI::JSON
  option :scheme,
         description: 'Metric naming scheme, text to prepend to metric',
         short: '-s SCHEME',
         long: '--scheme SCHEME',
         default: "memory_percent"

  def run
    # Based on memory-metrics.rb

    # Metrics borrowed from hoardd: https://github.com/coredump/hoardd

    output  metrics_hash

    ok
  end

  def metrics_hash
    mem = {}
    memp = {}

    meminfo_output.each_line do |line|
      mem['total']     = line.split(/\s+/)[1].to_i * 1024 if line.match(/^MemTotal/)
      mem['free']      = line.split(/\s+/)[1].to_i * 1024 if line.match(/^MemFree/)
      mem['buffers']   = line.split(/\s+/)[1].to_i * 1024 if line.match(/^Buffers/)
      mem['cached']    = line.split(/\s+/)[1].to_i * 1024 if line.match(/^Cached/)
      mem['swapTotal'] = line.split(/\s+/)[1].to_i * 1024 if line.match(/^SwapTotal/)
      mem['swapFree']  = line.split(/\s+/)[1].to_i * 1024 if line.match(/^SwapFree/)
      mem['dirty']     = line.split(/\s+/)[1].to_i * 1024 if line.match(/^Dirty/)
    end

    mem['swapUsed'] = mem['swapTotal'] - mem['swapFree']
    mem['used'] = mem['total'] - mem['free']
    mem['usedWOBuffersCaches'] = mem['used'] - (mem['buffers'] + mem['cached'])
    mem['freeWOBuffersCaches'] = mem['free'] + (mem['buffers'] + mem['cached'])

    # to prevent division by zero
    if mem['swapTotal'] == 0
      swptot = 1
    else
      swptot = mem['swapTotal']
    end

    mem.each do |k, _v|
      # with percentages, used and free are exactly complementary
      # no need to have both
      # the one to drop here is "used" because "free" will
      # stack up neatly to 100% with all the others (except swapUsed)
      # #YELLOW
      memp["#{config[:scheme]}_#{k}"] = (100.0 * mem[k] / mem['total']).round if k != 'total' && k !~ /swap/ && k != 'used'

      # with percentages, swapUsed and swapFree are exactly complementary
      # no need to have both
      memp["#{config[:scheme]}_#{k}"] = (100.0 * mem[k] / swptot).round if k != 'swapTotal' && k =~ /swap/ && k != 'swapFree'
    end

    memp
  end

  def meminfo_output
    File.open('/proc/meminfo', 'r')
  end
end
