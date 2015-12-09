#! /usr/bin/env ruby
#
#   cpu-metrics
#
# DESCRIPTION:
#   Sends total, user, nice, system, idle, iowait, irq, softirq, steal, guest
#   cpu stats as a sensu event.
#
# OUTPUT:
#   JSON
#
# PLATFORMS:
#   Linux
#
# DEPENDENCIES:
#   gem: sensu-plugin
#
# USAGE:
#   ./cpu-metrics.rb
#
# NOTES:
#
#
# * Original file located at:
# https://github.com/sensu/sensu-community-plugins/blob/master/plugins/system/check-cpu.rb
# * Modifications by Stanley Karunditu <stanleyk@cumulusnetworks.com>
#   - Convert Script to use JSON output
#   - Convert script from a standard check plugin to a metric plugin
#
# LICENSE:
#   Copyright 2014 Sonian, Inc. and contributors. <support@sensuapp.org>
#   Released under the same terms as Sensu (the MIT license); see LICENSE
#   for details.
#

require 'rubygems' if RUBY_VERSION < '1.9.0'
require 'sensu-plugin/metric/cli'
require 'json'

class CpuMetrics < Sensu::Plugin::Metric::CLI::JSON
  option :warn,
         short: '-w WARN',
         proc: proc(&:to_f),
         default: 80

  option :crit,
         short: '-c CRIT',
         proc: proc(&:to_f),
         default: 100

  option :sleep,
         long: '--sleep SLEEP',
         proc: proc(&:to_f),
         default: 1

  [:user, :nice, :system, :idle, :iowait, :irq, :softirq, :steal, :guest].each do |metric|
    option metric,
           long: "--#{metric}",
           description: "Check cpu #{metric} instead of total cpu usage",
           boolean: true,
           default: false
  end

  def acquire_cpu_stats
    File.open('/proc/stat', 'r').each_line do |line|
      info = line.split(/\s+/)
      name = info.shift
      return info.map(&:to_f) if name.match(/^cpu$/)
    end
  end

  def run
    metrics = [:user, :nice, :system, :idle, :iowait, :irq, :softirq, :steal, :guest]

    cpu_stats_before = acquire_cpu_stats
    sleep config[:sleep]
    cpu_stats_after = acquire_cpu_stats

    # Some kernels don't have a 'guest' value (RHEL5).
    metrics = metrics.slice(0, cpu_stats_after.length)

    cpu_total_diff = 0.to_f
    cpu_stats_diff = []
    metrics.each_index do |i|
      cpu_stats_diff[i] = cpu_stats_after[i] - cpu_stats_before[i]
      cpu_total_diff += cpu_stats_diff[i]
    end

    cpu_stats = []
    metrics.each_index do |i|
      cpu_stats[i] = 100 * (cpu_stats_diff[i] / cpu_total_diff)
    end

    cpu_usage = 100 * (cpu_total_diff - cpu_stats_diff[3]) / cpu_total_diff
    checked_usage = cpu_usage

    metrics.each do |metric|
      if config[metric]
        self.class.check_name "CheckCPU #{metric.to_s.upcase}"
        checked_usage = cpu_stats[metrics.find_index(metric)]
      end
    end

    outputstats = {}
    outputstats[:total] = (cpu_usage * 100).round / 100.0
    cpu_stats.each_index { |i| outputstats[metrics[i]] = (cpu_stats[i] * 100).round / 100.0 }
    output outputstats.to_json
    ok
  end
end
