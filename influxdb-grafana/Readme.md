There are a couple of dependencies to be aware of:

* Ensure you've either installed httplib2 or are using Ansible 2.x
* The following ports must be available on your local server
 - 3000 for Grafana
 - 8083 for Influxdb WebUI
 - 8086 for Influxdb API Agent
 Failure to open these ports will cause Vagrant to fail. If alternative ports are required, edit the following lines in the Vagrantfile
 ```
    # Grafana Port
    server1.vm.network "forwarded_port", guest: 3000, host: 3000

    # Influxdb Ports.
    server1.vm.network "forwarded_port", guest: 8083, host: 8083
    server1.vm.network "forwarded_port", guest: 8086, host: 8086
```
Replacing the `host` value with the port to be used on your local machine.

To Access the Monitoring demo:
* http://localhost:3000 - grafana dashboard. admin/admin to login
* http://localhost:8083 - influxdb dashboard.