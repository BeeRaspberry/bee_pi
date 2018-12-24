#!/usr/bin/env bash

function setup_prereqs() {
    python3 -m venv ${VIRTUALENV}
    source ${VIRTUALENV}/bin/activate
    pip install -r requirements.txt
    python find_probes.py
    if [[ $? -eq 0 ]]; then
       python cmd_config.py
    else
       RC=1
    fi
}

function setup_service() {
    touch ${INIT_FILE}
    chmod 0700 ${INIT_FILE}

    touch ${CONF_FILE}
    chmod 0700 ${CONF_FILE}


cat << EOF > ${INIT_FILE}
[Unit]
Description=Bee Data Record Service
After=network.target

[Service]
User=${SUDO_USER}
Group=pi
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=bee_data
Environment=VIRTUAL_ENV=${VIRTUALENV}
Environment=PATH=${VIRTUAL_ENV}/bin:${PATH}
Environment=DATA_DIR=${HOME_DIR}/bee_data
ExecStart=${VIRTUALENV}/bin/python ${HOME_DIR}/git/bee_pi/record_data.py
Restart=always

[Install]
WantedBy=multi-user.target

EOF
}
cat << 'EOF' > ${CONF_FILE
if $programname == "bee_data" then /var/log/bee_data.log
if $programname == "cmd_config" then /var/log/bee_cmd_config.log
if $programname == "find_probes" then /var/log/bee_find_probes.log

EOF

   systemctl restart rsyslog
   systemctl daemon-reload
   systemctl start bee_data
}

RC=0
INIT_FILE=/usr/lib/systemd/system/bee_data.service
CONF_FILE=/etc/rsyslog.d/bee_data.conf
HOME_DIR=/home/${SUDO_USER}
VIRTUALENV=${HOME_DIR}/virtualenv

[[ ! -d ${HOME_DIR}/bee_data ]] && mkdir ${HOME_DIR}/bee_data

setup_prereqs
if [[ ${RC} -eq 0 ]]; then
   setup_service
fi