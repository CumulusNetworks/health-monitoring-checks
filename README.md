# **This directory contains health check plugins and check definitions which are still being developed and are still in the alpha testing stage.**

# Cumulus Health Monitoring Checks

The check plugins defined in this repo are designed to work in Nagios, Sensu,
Consul and any other Nagios compatible health monitoring system that can run
on Cumulus Linux

## Directory Structure

* Plugins: List of Health monitoring plugins written mainly in BASH and Python
* Sensu: Sensu Configuration json file examples using the plugins found in this
  directory. The list of checks configured are a list suggested by Cumulus
Networks.


###CONTRIBUTING


1. Fork it.
2. Create your feature branch (`git checkout -b my-new-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin my-new-feature`).
5. Create new Pull Request.

## License and Authors

* Author:: Cumulus Networks Inc.

* Copyright:: 2015 Cumulus Networks Inc.

Licensed under the MIT License.


### TODO
Upstream the new and/or heavily monitoring checks to [Nagios Exchange](https://exchange.nagios.org/)


---

![Cumulus icon](http://cumulusnetworks.com/static/cumulus/img/logo_2014.png)

### Cumulus Linux

Cumulus Linux is a software distribution that runs on top of industry standard
networking hardware. It enables the latest Linux applications and automation
tools on networking gear while delivering new levels of innovation and
ﬂexibility to the data center.

For further details please see:
[cumulusnetworks.com](http://www.cumulusnetworks.com)

