#!/usr/bin/python

import sys
import json
import subprocess



#Datastructure
class ExportData(object):
    """
    This datastructure holds all data needed for an output routine.
    Data will be serialized from this datastructure as it is exported
    by different output modules for each data receiver (influxdb, logstash,
    http, etc.)
    """

    def __init__(self, tag, hostname, unique_id_type):
        self.tag = str(tag)
        self.hostname = str(hostname)
        self.unique_id_type=str(unique_id_type)
        self.data = {}

    def add_variable(self, variable_name):
        self.data[variable_name] = {}


    def add_value(self, variable_name, unique_id, value):
        #if variable_name not in self.data:
        #    self.data[variable_name] = {}
        if unique_id not in self.data[variable_name]:
            self.data[variable_name][unique_id] = []
        self.data[variable_name][unique_id].append(value)

    def show_variables(self):
        print "Known Variables for (%s):" % self.tag
        for variable in self.data:
            print "    %s" % variable

    def show_data(self):
        output= "data is tagged with: %s \n" % self.tag
        output+="    %s data for host: %s\n" % (self.unique_id_type,self.hostname)
        count=0
        for variable in self.data:
            count +=1
            for unique_id in self.data[variable]:
                for value in self.data[variable][unique_id]:
                    tab_space = '\t' * count
                    output += "%15s%s%s=%s\n" % (unique_id,tab_space,variable,value)  
        print output


    def __repr__(self):
        output=""
        for variable in self.data:
            for unique_id in self.data[variable]:
                for value in self.data[variable][unique_id]:
                    output += "%s,host=%s,%s=%s %s=%s\n" % (self.tag,self.hostname,self.unique_id_type,unique_id,variable,value)  
        return output


Supported_Arguments=[
"interface_state",
"interface_stats",
]

def usage():
    print "   Usage: %s [%s]" % (sys.argv[0], "|".join(Supported_Arguments))
    exit(1)

#Parse Arguments
if len(sys.argv)!=2:
    print "ERROR: Need a single argument."
    usage()
if sys.argv[1] not in Supported_Arguments:
    usage()


#Collect Generic Info Used in All Modules
hostname=subprocess.check_output(['/bin/hostname'],shell=True).replace("\n","")
output=None

#Collection Modules
#   These could be broken off into different files.
if sys.argv[1] == "interface_state":
    """
    Collects the linkstate and speed of running interfaces.
    """
    output=subprocess.check_output(['/usr/bin/netshow interface all -j'],shell=True)
    parsed_output=json.loads(output)
    #data = ExportData(tag,hosname,unique_id_type)
    data = ExportData("iface_state",hostname,"interface")
    data.add_variable("linkstate")
    data.add_variable("speed")

    for item in parsed_output:
        #data.add_value(variable,unique_id,value)
        data.add_value("linkstate",item,parsed_output[item]['linkstate'])
        data.add_value("speed",item,parsed_output[item]['speed'])


elif sys.argv[1] == "interface_stats":
    """
    Collects packets transmitted and dropped in the RX/TX directions.
    """
    output=subprocess.check_output(['/usr/cumulus/bin/cl-netstat -j'],shell=True)
    parsed_output=json.loads(output)
    #data = ExportData(tag,hosname,unique_id_type)
    data = ExportData("iface_stats",hostname,"interface")
    data.add_variable("RX_OK")
    data.add_variable("TX_OK")
    data.add_variable("RX_DRP")
    data.add_variable("TX_DRP")

    for item in parsed_output:
        #data.add_value(variable,unique_id,value)
        data.add_value("RX_OK",item,parsed_output[item]['RX_OK'])
        data.add_value("TX_OK",item,parsed_output[item]['TX_OK'])
        data.add_value("RX_DRP",item,parsed_output[item]['RX_DRP'])
        data.add_value("TX_DRP",item,parsed_output[item]['TX_DRP'])

else:
    print "ERROR: Unrecognized argument."

#Use these to sanity check the datastructure
print "######################"
print "   Sanity checking:"
print "######################"
data.show_variables()
data.show_data()

#Generic CLI Output Serializer
print "#####################################"
print "     Sample CLI Output Serializer:"
print "#####################################"
print data

exit(0)