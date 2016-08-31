
Step 1: install fluentd using these steps: http://docs.fluentd.org/articles/install-by-deb#step-1--install-from-apt-repository

curl -L https://toolbelt.treasuredata.com/sh/install-debian-jessie-td-agent2.sh | sh


Step 2: install influxdb output plugin using these steps: /usr/sbin/td-agent-gem install fluent-plugin-influxdb

Step 3: configure influxdb using td-agent.conf file.

After this, ALL syslogs will start being written to influxdb to the measurement named 'log'.