#! /usr/bin/env ruby
#  encoding: UTF-8
#
#   disk-usage-metrics
#
# DESCRIPTION:
#   This plugin uses df to collect disk capacity metrics
#   disk-usage-metrics.rb looks at /proc/stat which doesnt hold capacity metricss.
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
#
# USAGE:
#
# NOTES:
#   Based on disk-capacity-metrics.rb by bhenerey and nstielau
#   The difference here being how the key is defined in graphite and the
#   size we emit to graphite(now using megabytes). Also i dropped inode info.
#   Using this as an example
#   Filesystem                                 Size  Used Avail Use% Mounted on
#   /dev/mapper/precise64-root                  79G  3.5G   72G   5% /
#   /dev/sda1                                  228M   25M  192M  12% /boot
#   /dev/sdb1                                   99G    2G   97G   2% /media/sda1
#   The keys with this plugin will be
#    disk_usage.root, disk_usage.root.boot, and disk_usage.root.media.sda1
#    instead of disk.dev.mapper.precise64-root, disk.sda1, and disk.sda2
#
#   Use --flatten option to reduce graphite "tree" by using underscores rather
#   then dots for subdirs. Also eliminates 'root' on mounts other than '/'.
#   Keys with --flatten option would be
#    disk_usage.root, disk_usage.boot, and disk_usage.media_sda1
#
#   Mountpoints can be specifically included or ignored using -i or -I options:
#     e.g. disk-usage-metric.rb -i ^/boot,^/media
#
#   Original file converted by Stanley Karunditu <stanleyk@cumulusnetworks.com>
#   to use JSON instead of Graphite format
# LICENSE:
#   Copyright 2012 Sonian, Inc <chefs@sonian.net>
#   Released under the same terms as Sensu (the MIT license); see LICENSE
#   for details.
#

require 'sensu-plugin/metric/cli'
require 'socket'

#
# Disk Usage Metrics
#
class DiskUsageMetrics < Sensu::Plugin::Metric::CLI::JSON
  option :scheme,
         description: 'Metric naming scheme, text to prepend to .$parent.$child',
         long: '--scheme SCHEME',
         default: "disk_usage"
  option :ignore_mnt,
         description: 'Ignore mounts matching pattern(s)',
         short: '-i MNT[,MNT]',
         long: '--ignore-mount',
         proc: proc { |a| a.split(',') }

  option :include_mnt,
         description: 'Include only mounts matching pattern(s)',
         short: '-I MNT[,MNT]',
         long: '--include-mount',
         proc: proc { |a| a.split(',') }

  option :flatten,
         description: 'Output mounts with underscore rather than dot',
         short: '-f',
         long: '--flatten',
         boolean: true,
         default: false

  option :local,
         description: 'Only check local filesystems (df -l option)',
         short: '-l',
         long: '--local',
         boolean: true,
         default: true

  option :block_size,
         description: 'Set block size for sizes printed',
         short: '-B BLOCK_SIZE',
         long: '--block-size BLOCK_SIZE',
         default: 'M'

  # Main function
  #
  def run
    delim = config[:flatten] == true ? '_' : '.'
    # Get disk usage from df with used and avail in megabytes
    # #YELLOW
    `df -PB#{config[:block_size]} #{config[:local] ? '-l' : ''}`.split("\n").drop(1).each do |line|
      _, _, used, avail, used_p, mnt = line.split
      diskspace = {}
      prefix_str = 'disk_usage'
      unless %r{/sys|/dev|/run}.match(mnt)
        next if config[:ignore_mnt] && config[:ignore_mnt].find { |x| mnt.match(x) }
        next if config[:include_mnt] && !config[:include_mnt].find { |x| mnt.match(x) }
        if config[:flatten]
          mnt = mnt.eql?('/') ? 'root' : mnt.gsub(/^\//, '')
        else
          # If mnt is only / replace that with root if its /tmp/foo
          # replace first occurance of / with root.
          mnt = mnt.length == 1 ? 'root' : mnt.gsub(/^\//, 'root.')
        end
        # Fix subsequent slashes
        mnt = mnt.gsub '/', delim
        diskspace[[config[:scheme],  'used'].join('_')] = used.gsub(config[:block_size], '').to_i
        diskspace[[config[:scheme],  'avail'].join('_')] = avail.gsub(config[:block_size], '').to_i
        diskspace[[config[:scheme],  'used_percentage'].join('_')] = used_p.gsub(config[:block_size], '').to_i
        output diskspace
      end
    end
    ok
  end
end
