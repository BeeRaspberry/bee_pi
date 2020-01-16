#!/usr/bin/env bash

function install_package() {
    PKG=$1
    apt list --installed | grep -i ${PKG} 2>/dev/null
    if [[ $? -ne 0 ]]; then
        echo "${PKG} not found ... Installing"
        apt install ${PKG} -y
    else
        echo "${PKG} already installed"
    fi
}

function install_adafruit() {
    echo "Checking Adafruit"
    cd /tmp
    if [[ ! -d "/tmp/Adafruit_Python_DHT" ]]; then
        git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    fi
    cd Adafruit_Python_DHT
    git pull
    python setup.py install
}

function install_python() {
    echo "Install Python 3 requirements"
    for FILE in python3 python3-pip python3-venv git-core build-essential python3-dev python3-setuptools
    do
      install_package ${FILE}
    done
}

function copy_files() {
    if [[ ! -d "${BEE_SRC}" ]]; then
        mkdir -p ${BEE_SRC}
    fi

    cd ${WORKING_DIR}
    for FILE in cmd_config.py config.py record_data.py find_probes.py install.sh pi_requirements.txt
    do
        cp ${FILE} ${BEE_SRC}/.
    done
}

function setup_virtualenv() {
    echo "Creating virtualenv ${VIRTUALENV}"
    cd ${WORKING_DIR}
    [[ ! -d ${BEE_DATA} ]] && python3 -m venv ${VIRTUALENV}

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
Environment=CONFIG_FILE=${BEE_DIR}/config.json
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
    if [[ ! -f ${INIT_FILE} ]]; then
        create_init_file
    fi

    if [[ ! -f ${CONF_FILE} ]]; then
        create_conf_file
    fi

   systemctl restart rsyslog
   systemctl daemon-reload
   systemctl start bee_data
   systemctl enable bee_data
}

if (( $EUID != 0 )); then
    echo "Script needs to be run as root"
    exit 9
fi

RC=0
WORKING_DIR="$( dirname "${BASH_SOURCE[0]}" )"

[ -z ${INIT_FILE+x} ] && INIT_FILE=/etc/systemd/system/bee_data.service
[ -z ${CONF_FILE+x} ] && CONF_FILE=/etc/rsyslog.d/bee_data.conf
[ -z ${BEE_DIR+x} ] && BEE_DIR=/opt/bee_pi
BEE_DATA=${BEE_DIR}/bee_data
BEE_SRC=${BEE_DIR}/src
export CONFIG_FILE=${BEE_DIR}/config.json
VIRTUALENV=${BEE_DIR}/virtualenv

[[ ! -d ${BEE_DATA} ]] && mkdir -p ${BEE_DATA}

apt-get update && apt-get upgrade -y
install_python && install_adafruit
copy_files && setup_virtualenv

echo "Fix permissions"
chown -R pi:pi ${BEE_DIR}
setup_service
exit $RC
