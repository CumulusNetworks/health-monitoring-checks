#!/usr/bin/python

from socket import gethostname

#Datastructure
class ExportData(object):
    """
    This datastructure holds all data needed for an output routine.
    Data will be serialized from this datastructure as it is exported
    by different output modules for each data receiver (influxdb, logstash,
    http, etc.)

    | data_set_name |   {fixed_tags}    |     {data}       |

    example:
    | "iface_state" | {"host":"leaf01"} | {"interface":"eth0","linkstate":"up"} |

    """

    def __init__(self, data_set_name, fixed_tags, data=None):
        self.data_set_name = str(data_set_name)
        self.fixed_tags=fixed_tags
        #'host' tag is always populated by the datastructure
        self.fixed_tags['host']=gethostname()
        # data can optionally be provided in a dict upon DS declaration
        if data==None: self.data = []
        elif type(data) is dict: self.data = [data]
        else:
            print "ERROR: if passing data, type must be a dict!"
            exit(1)

    def show_data(self):
        """
        Used for debugging purposes, this function displays data in a human readable format.
        """
        output = "######################\n"
        output+= "   Sanity checking:\n"
        output+= "######################\n"
        output+= "<data set name is: %s >\n" % self.data_set_name
        output+= "    data has fixed tags: \n        "
        output+= "%s \n" % (self.__fixed_tags())
        output+= "    data is: \n        "
        for data_element in self.data:
            for data_column in data_element:
                output += "%s=%s, " %(data_column,data_element[data_column])
            output += "\n        "
        #output += "%15s%s%s=%s\n"
        print output

    def add_row(self,data):
        if type(data) is not dict:
            print "ERROR: Data must be provided in Dictionary!"
            exit(1)
        self.data.append(data)

    def send_data(self,recipients):
        """
        This function defines which targets will receive the data.
        """
        targets = recipients.split(',')
        for target in targets:
            if target == "cli": print self
            else:
                print "ERROR: Method %s not implemented!" % target
                exit(1)

    def __fixed_tags(self):
        fixed_tags=""
        for tag in self.fixed_tags:
            fixed_tags+= "%s=%s," % (tag,self.fixed_tags[tag])
        return fixed_tags

    def __repr__(self):
        output=""
        for data_element in self.data:
            data = ""
            for data_column in data_element:
                data += " %s=%s" % (data_column,data_element[data_column])
            output += "%s,%s%s\n" % (self.data_set_name,self.__fixed_tags(),data)
        return output
