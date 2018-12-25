#!/usr/bin/env bash

function setup_python3() {
    echo "Checking Python3"
    python3 --version >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        apt-get install python3
    fi
}

function copy_files() {
    if [[ ! -d "${BEE_SRC}" ]]; then
        mkdir -p ${BEE_SRC}
    fi

    for FILE in cmd_config.py config.py record_data.py gui_config.py install.sh setup.py
    do
        cp ${FILE} ${BEE_SRC}/.
    done
}

function setup_prereqs() {
    echo "Creating virtualenv ${VIRTUALENV}"
    if [[ ! -d "${VIRTUALENV}" ]]; then
      python3 -m venv ${VIRTUALENV}
    fi
    echo "Installing python requirements"
    source ${VIRTUALENV}/bin/activate
    pip install -r pi_requirements.txt
    echo "Searching for probes"
    python find_probes.py
    if [[ $? -eq 0 ]]; then
       python cmd_config.py
    else
       RC=1
    fi
}

function create_init_file() {
    touch ${INIT_FILE}
    chmod 0700 ${INIT_FILE}

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
Environment=DATA_DIR=${BEE_DATA}
ExecStart=${VIRTUALENV}/bin/python ${BEE_SRC}/record_data.py
Restart=always

[Install]
WantedBy=multi-user.target

EOF
}

function create_conf_file() {
    touch ${CONF_FILE}
    chmod 0700 ${CONF_FILE}

cat << 'EOF' > ${CONF_FILE}
if $programname == "bee_data" then /var/log/bee_data.log
if $programname == "cmd_config" then /var/log/bee_cmd_config.log
if $programname == "find_probes" then /var/log/bee_find_probes.log

EOF

}

function setup_service() {
    echo "Adding service"
    if [[ ! -f ${CONF_FILE} ]]; then
        create_init_file
    fi

    if [[ ! -f ${CONF_FILE} ]]; then
        create_conf_file
    fi

   systemctl restart rsyslog
   systemctl daemon-reload
   systemctl start bee_data
}

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit
fi

RC=0
INIT_FILE=/usr/lib/systemd/system/bee_data.service
CONF_FILE=/etc/rsyslog.d/bee_data.conf
BEE_DIR=/opt/bee_pi
BEE_DATA=${BEE_DIR}/bee_data
BEE_SRC=${BEE_DIR}/src
VIRTUALENV=${BEE_DIR}/virtualenv

[[ ! -d ${BEE_DATA} ]] && mkdir -p ${BEE_DATA}

copy_files
setup_prereqs
if [[ ${RC} -eq 0 ]]; then
   setup_service
fi