#! /usr/bin/env ruby
#  encoding: UTF-8
#
#   check-memory
#
# DESCRIPTION:
#   Sends a critical or warning alert if RAM exceeds the set threshold
#
# OUTPUT:
#   plain text
#
# PLATFORMS:
#   Linux
#
# DEPENDENCIES:
#   gem: sensu-plugin
#
# USAGE:
#  Sends out a warning sensu event if CPU is greater than 90%
#   ./check-memory.rb -w 90
#
#
# NOTES:
#   - Original file is from
#   https://raw.githubusercontent.com/sensu/sensu-community-plugins/master/plugins/system/check-ram.rb
#   - Modified by Stanley Karunditu <stanleyk@cumulusnetwork.com> to set warning
#   and critical levels based on used RAM not on RAM left. Seems to make more
#   sense this way and the CPU and Disk checks work the same way too. Removed
#   check what megabytes are left. Renamed file to check-memory. More consistent
#   with other check names in this repo
#
# LICENSE:
#   Copyright 2012 Sonian, Inc <chefs@sonian.net>
#   Released under the same terms as Sensu (the MIT license); see LICENSE
#   for details.
#
require 'rubygems' if RUBY_VERSION < '1.9.0'
require 'sensu-plugin/check/cli'

class CheckRAM < Sensu::Plugin::Check::CLI
  option :warn,
         short: '-w WARN',
         proc: proc(&:to_i),
         default: 90

  option :crit,
         short: '-c CRIT',
         proc: proc(&:to_i),
         default: 95

  def run
    total_ram, free_ram, used_ram = 0, 0, 0

    if `free --help` =~ /.*wide output.*/
      `free -mw`.split("\n").drop(1).each do |line|
        free_ram = line.split[7].to_i if line =~ /^Mem:/
        total_ram = line.split[1].to_i if line =~ /^Mem:/
      end
    else
      `free -m`.split("\n").drop(1).each do |line|
        free_ram = line.split[3].to_i if line =~ /^-\/\+ buffers\/cache:/ # rubocop:disable RegexpLiteral
        total_ram = line.split[1].to_i if line =~ /^Mem:/
      end
    end

    used_ram = total_ram - free_ram

    unknown 'invalid percentage' if config[:crit] > 100 || config[:warn] > 100
    percents_used = used_ram * 100 / total_ram
    percents_left = free_ram * 100 / total_ram
    message "#{percents_left}% free RAM left"

    critical if percents_used > config[:crit]
    warning if percents_used > config[:warn]
    ok
  end
end
