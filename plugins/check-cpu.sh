#!/bin/bash
#
# check-cpu
#
# DESCRIPTION
#   Check CPU Usage
#
# OUTPUT
#    plain text
#
# PLATFORMS:
#    Linux
#
# DEPENDENCIES:
#    Bash
#
# USAGE:
#   check-cpu.sh -w 85 -c 95
#
# NOTES:
#    Amended by Stanley Karunditu <stanleyk@cumulusnetworks.com> to include
#    top 5 processes when a warning or critical message is printed
#
# LICENSE:
#   Date: 2014-09-12
#   Author: Jun Ichikawa <jun1ka0@gmail.com>
#
#   Released under the same terms as Sensu (the MIT license); see LICENSE
#   for details.
#
# get arguments
while getopts 'w:c:h' OPT; do
  case $OPT in
    w)  WARN=$OPTARG;;
    c)  CRIT=$OPTARG;;
    h)  hlp="yes";;
    *)  unknown="yes";;
  esac
done

# usage
HELP="
    usage: $0 [ -w value -c value -p -h ]

        -w --> Warning percentage < value
        -c --> Critical percentage < value
        -h --> print this help screen
"

if [ "$hlp" = "yes" ]; then
  echo "$HELP"
  exit 0
fi

cpuusage1=(`cat /proc/stat | head -1`)
if [ ${#cpuusage1} -eq 0 ]; then
  echo "CRITICAL - CPU UNKNOWN"
  exit 2
fi
sleep 1
cpuusage2=(`cat /proc/stat | head -1`)
if [ ${#cpuusage2} -eq 0 ]; then
  echo "CRITICAL - CPU UNKNOWN"
  exit 2
fi

WARN=${WARN:=90}
CRIT=${CRIT:=95}

cpu_diff=(0)
total=0
usage_diff=0
for i in `seq 1 9`
do
  cpu_diff=("${cpu_diff[@]}" `echo "${cpuusage2[$i]}-${cpuusage1[$i]}" | bc`)
  total=`echo "$total+${cpu_diff[$i]}" | bc`
  if [ $i -ne "4" ]; then
    usage_diff=`echo "$usage_diff+${cpu_diff[$i]}" | bc`
  else
    idl=$cpu_diff[$i]
  fi
done
cpu_usage=`echo "scale=2; 100*$usage_diff/$total" | bc`
top_5=`ps -e -o pcpu,comm,pid | sort -n -r | grep -v "%CPU" | head -5 | awk \
'{print $1 "%==" $2 }'  | paste -d, -s -`
if [ "$(echo "${cpu_usage} > ${CRIT}" | bc)" -eq 1 ]; then
  echo "CPU CRITICAL - Current Usage:${cpu_usage}% > ${CRIT}% [Top 5 Proc: $top_5]"
  exit 2
fi

if [ "$(echo "${cpu_usage} > ${WARN}" | bc)" -eq 1 ]; then
  echo "CPU WARNING - Current Usage:${cpu_usage}% > ${WARN}% [Top 5 Proc: $top_5]"
  exit 1
fi

echo "CPU OK - Usage:${cpu_usage}"
exit 0
