#!/usr/bin/env bash

INIT_FILE=/lib/systemd/system/bee_data.service
touch $INIT_FILE
chmod 0700 $INIT_FILE

CONF_FILE=/etc/rsyslog.d/bee_data.conf
touch $CONF_FILE
chmod 0700 $CONF_FILE

HOME_DIR=/home/$SUDO_USER
mkdir $HOME_DIR/bee_data

cat << 'EOF' > $INIT_FILE
[Unit]
Description=Bee Data Record Service
After=network.target
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=bee_data

[Service]
User=$SUDO_USER
Group=pi
Environment=VIRTUAL_ENV=$HOME_DIR/virtualenv
Environment=PATH=$VIRTUAL_ENV/bin:$PATH
Environment=DATA_DIR=$HOME_DIR/bee_data
ExecStart=$HOME_DIR/virtualenv/bin/python $HOME_DIR/git/bee_pi/record_data.py
Restart=always

[Install]
WantedBy=multi-user.target

EOF

cat << 'EOF' > $CONF_FILE
if $programname == "bee_data" then /var/log/bee_data.log
if $programname == "cmd_config" then /var/log/bee_cmd_config.log
if $programname == "find_probes" then /var/log/bee_find_probes.log

EOF

systemctl restart rsyslog
systemctl daemon-reload
systemctl start bee_data
