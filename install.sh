#!/usr/bin/env bash
set -x
function setup_prereqs() {
    python3 -m venv $VIRTUALENV
    source $VIRTUALENV/bin/activate
    pip install -r requirements.txt
    python find_probes.py
    if [ $? -eq 0 ]; then
       python cmd_config.py
    else
       RC=1
    fi
}

function_write_wlan_file() {
cat << EOF > /etc/network/interfaces.d/wlan
allow-hotplug wlan0
iface wlan0 inet static
   address 192.168.20.1
   netmask 255.255.255.0
   network 192.168.20.0

EOF

   service dhcpcd restart
   ifdown wlan0
   ifup wlan0
   echo "hello"
}

function configure_dhcp() {
   mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cat << EOF > /etc/dnsmasq.conf
interface=wlan0
usually wlan0
   dhcp-range=192.168.20.10,192.168.20.20,1h

EOF

}

function configure_hostapd() {
cat <<EOF >/etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=beepi
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=needtoaddvariable
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

EOF

   sed -i 's/#DAEMON_CONF=""/DAEMON_CONF="/etc/hostapd/hostapd.conf"/' \
      /etc/default/hostapd

   service hostapd start
   service dnsmasq start
   echo "hello"
}

function setup_ap() {
    dpkg --get-selections | grep dnsmasq >/dev/null \
	|| apt-get -y install dnsmasq
    dpkg --get-selections | grep hostapd >/dev/null \
        || apt-get -y install hostapd
    systemctl stop dnsmasq
    systemctl stop hostapd
    grep denyinterfaces /etc/dhcpcd.conf >/dev/null \
        || echo "denyinterfaces wlan0" >>/etc/dhcpcd.conf
    grep -r wlan /etc/network >/dev/null \
        || function_write_wlan_file
    [[ -f /etc/dnsmasq.conf.orig ]] \
        || configure_dhcp
    [[ -f /etc/hostapd/hostapd.conf ]] \
        || configure_hostapd
}

function setup_service() {
    touch $INIT_FILE
    chmod 0700 $INIT_FILE

    touch $CONF_FILE
    chmod 0700 $CONF_FILE


cat << EOF > $INIT_FILE
[Unit]
Description=Bee Data Record Service
After=network.target

[Service]
User=$SUDO_USER
Group=pi
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=bee_data
Environment=VIRTUAL_ENV=$VIRTUALENV
Environment=PATH=$VIRTUAL_ENV/bin:$PATH
Environment=DATA_DIR=$HOME_DIR/bee_data
ExecStart=$VIRTUALENV/bin/python $HOME_DIR/git/bee_pi/record_data.py
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
}

RC=0
INIT_FILE=/usr/lib/systemd/system/bee_data.service
CONF_FILE=/etc/rsyslog.d/bee_data.conf
HOME_DIR=/home/$SUDO_USER
VIRTUALENV=$HOME_DIR/virtualenv

[ ! -d $HOME_DIR/bee_data ] && mkdir $HOME_DIR/bee_data

#setup_prereqs
#if [ $RC -eq 0 ]; then
#   setup_service
#fi
setup_ap
