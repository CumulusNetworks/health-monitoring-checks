# -*- mode: ruby -*-
# vi: set ft=ruby :

groups = {
  "spines" => ["spine1", "spine2"],
  "leafs" => ["leaf1", "leaf2", "leaf3", "leaf4"],
  "servers" => ["server1", "server2", "server3"],
  "network:children" => ["spines", "leafs"],
  "xenials" => ["server1", "server2"]
}


Vagrant.configure("2") do |config|

  cumulus_image = "CumulusCommunity/VX-3.0"
  #server_image = "ubuntu/trusty64"
  server_image = "boxcutter/ubuntu1604"
  link_seed = "influxdb-grafana"

  config.vm.define "leaf1" do |leaf1|
    leaf1.vm.box = cumulus_image
    leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine1-' + link_seed, auto_config: false
    leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine2-' + link_seed, auto_config: false
    leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-server1-' + link_seed, auto_config: false
    leaf1.vm.host_name = "leaf1"

    leaf1.vm.provision "ansible" do |ansible|
      ansible.groups = groups
      #ansible.verbose = "vvv"
      ansible.playbook = "provision.yml"
    end

    leaf1.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nicpromisc2", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc3", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc4", "allow-vms"]
    end
  end

  config.vm.define "leaf2" do |leaf2|
    leaf2.vm.box = cumulus_image
    leaf2.vm.network "private_network",  virtualbox__intnet: 'leaf2-spine1-' + link_seed, auto_config: false
    leaf2.vm.network "private_network",  virtualbox__intnet: 'leaf2-spine2-' + link_seed, auto_config: false
    leaf2.vm.network "private_network",  virtualbox__intnet: 'leaf2-server1-' + link_seed, auto_config: false
    leaf2.vm.host_name = "leaf2"

    leaf2.vm.provision "ansible" do |ansible|
      ansible.groups = groups
      ansible.playbook = "provision.yml"
    end

    leaf2.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nicpromisc2", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc3", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc4", "allow-vms"]
    end
  end

  config.vm.define "leaf3" do |leaf3|
    leaf3.vm.box = cumulus_image
    leaf3.vm.network "private_network",  virtualbox__intnet: 'leaf3-spine1-' + link_seed, auto_config: false
    leaf3.vm.network "private_network",  virtualbox__intnet: 'leaf3-spine2-' + link_seed, auto_config: false
    leaf3.vm.network "private_network",  virtualbox__intnet: 'leaf3-server2-' + link_seed, auto_config: false
    leaf3.vm.host_name = "leaf3"

    leaf3.vm.provision "ansible" do |ansible|
      ansible.groups = groups
      ansible.playbook = "provision.yml"
    end

    leaf3.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nicpromisc2", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc3", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc4", "allow-vms"]
    end
  end

  config.vm.define "leaf4" do |leaf4|
    leaf4.vm.box = cumulus_image
    leaf4.vm.network "private_network",  virtualbox__intnet: 'leaf4-spine1-' + link_seed, auto_config: false
    leaf4.vm.network "private_network",  virtualbox__intnet: 'leaf4-spine2-' + link_seed, auto_config: false
    leaf4.vm.network "private_network",  virtualbox__intnet: 'leaf4-server2-' + link_seed, auto_config: false
    leaf4.vm.host_name = "leaf4"

    leaf4.vm.provision "ansible" do |ansible|
      ansible.groups = groups
      ansible.playbook = "provision.yml"
    end

    leaf4.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nicpromisc2", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc3", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc4", "allow-vms"]
    end
  end

  config.vm.define "spine1" do |spine1|
    spine1.vm.box = cumulus_image
    spine1.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine1-' + link_seed, auto_config: false
    spine1.vm.network "private_network",  virtualbox__intnet: 'leaf2-spine1-' + link_seed, auto_config: false
    spine1.vm.network "private_network",  virtualbox__intnet: 'leaf3-spine1-' + link_seed, auto_config: false
    spine1.vm.network "private_network",  virtualbox__intnet: 'leaf4-spine1-' + link_seed, auto_config: false
    spine1.vm.host_name = "spine1"

    spine1.vm.provision "ansible" do |ansible|
      ansible.groups = groups
      ansible.playbook = "provision.yml"
    end

    spine1.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nicpromisc2", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc3", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc4", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc5", "allow-vms"]
    end
  end

  config.vm.define "spine2" do |spine2|
    spine2.vm.box = cumulus_image
    spine2.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine2-' + link_seed, auto_config: false
    spine2.vm.network "private_network",  virtualbox__intnet: 'leaf2-spine2-' + link_seed, auto_config: false
    spine2.vm.network "private_network",  virtualbox__intnet: 'leaf3-spine2-' + link_seed, auto_config: false
    spine2.vm.network "private_network",  virtualbox__intnet: 'leaf4-spine2-' + link_seed, auto_config: false
    spine2.vm.host_name = "spine2"

    spine2.vm.provision "ansible" do |ansible|
      ansible.groups = groups
      ansible.playbook = "provision.yml"
    end

    spine2.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nicpromisc2", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc3", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc4", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc5", "allow-vms"]
    end

  end

  config.vm.define "server1" do |server1|
    server1.vm.box = server_image
    server1.vm.network "private_network",  virtualbox__intnet: 'leaf1-server1-' + link_seed, auto_config: false
    server1.vm.network "private_network",  virtualbox__intnet: 'leaf2-server1-' + link_seed, auto_config: false
    # Grafana Port
    server1.vm.network "forwarded_port", guest: 3000, host: 3000

    # Influxdb Ports.
    server1.vm.network "forwarded_port", guest: 8083, host: 8083
    server1.vm.network "forwarded_port", guest: 8086, host: 8086

    server1.vm.host_name = "server1"

    server1.vm.provision "ansible" do |ansible|
      ansible.groups = groups
      ansible.playbook = "provision.yml"
    end

    server1.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--nicpromisc2", "allow-vms"]
      v.customize ["modifyvm", :id, "--nicpromisc3", "allow-vms"]
    end
  end

 config.vm.define "server2" do |server2|
   server2.vm.box = server_image
   server2.vm.network "private_network",  virtualbox__intnet: 'leaf3-server2-' + link_seed, auto_config: false
   server2.vm.network "private_network",  virtualbox__intnet: 'leaf4-server2-' + link_seed, auto_config: false
   server2.vm.host_name = "server2"

   server2.vm.provision "ansible" do |ansible|
     ansible.groups = groups
     ansible.playbook = "provision.yml"
   end

   server2.vm.provider "virtualbox" do |v|
     v.customize ["modifyvm", :id, "--nicpromisc2", "allow-vms"]
     v.customize ["modifyvm", :id, "--nicpromisc3", "allow-vms"]
   end
 end
end
