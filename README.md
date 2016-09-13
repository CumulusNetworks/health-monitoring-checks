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


Quickstart: Run the demo
------------------------
(This assumes you are running Ansible 1.9.4 and Vagrant 1.8.4 on your host.)

    Create the virtual network:
    git clone https://github.com/cumulusnetworks/cldemo-vagrant
    cd cldemo-vagrant
    vagrant up oob-mgmt-server oob-mgmt-switch leaf01 leaf02 leaf03 leaf04 spine01 spine02 server01 server02 server03 server04
    vagrant ssh oob-mgmt-server
    sudo su - cumulus
    sudo apt-get install software-properties-common -y
    sudo apt-add-repository ppa:ansible/ansible -y
    sudo apt-get update
    sudo apt-get install ansible -qy
    -
    Setting up the base network:
    git clone https://github.com/cumulusnetworks/cldemo-automation-ansible
    cd cldemo-automation-ansible
    git checkout full-reference-topology
    ansible-playbook run-demo.yml
    ssh server01
    wget 172.16.2.101
    cat index.html
    exit to oob-mgmt-server
    -
    Specific to Monitoring:
    cd..
    git clone https://github.com/CumulusNetworks/health-monitoring-checks/
    cd health-monitoring-checks/
    git checkout influx-grafana
    cd cldemo
    ansible-playbook main.yml

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

