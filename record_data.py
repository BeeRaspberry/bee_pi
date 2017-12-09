# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
from datetime import datetime
import Adafruit_DHT
import netifaces
import json
import requests
import logging
from urllib.request import urlopen

DEBUG = 1
# Setup the pins we are connect to
RCpin = 24
DHTpin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = logging.getLogger('record_data')


def checkForNetworkConnection():
    networkConnected = False
    interfaces = netifaces.interfaces()
    for interface in netifaces.interfaces():
        addr = netifaces.ifaddresses(interface)
        if addr[netifaces.AF_INET] != '' and \
                addr[netifaces.AF_INET] != '127.0.0.1':
            networkConnected = True
    return networkConnected


def connectDB():
    db_filename = 'beedata.db'
    db_is_new = not os.path.exists(db_filename)

    global conn
    conn = sqlite3.connect(db_filename)

    if db_is_new:
        print('create db')


def loadConfig(file_name):
    config_exists = os.path.exists(file_name)
    global settings

    if config_exists:
        with open(file_name) as data_file:
            return json.load(data_file)
    else:
        return None


def writeData(filename, hiveData):
    print(filename)
    with open(filename, 'a') as data_file:
        for probe in hiveData['probes']:
            line = '{},{},{},{},{},{}\n'.format(hiveData['hive']['id'],
                datetime.utcnow(), probe['model'], probe['outdoor'],
                probe['temperature'], probe['humidity'])
            data_file.write(line)


def postDB(hiveData, filename):
    if settings['DataStore'] == 'File':
        writeData(hiveData)


def main():
    print('starting...')
#    network = checkForNetworkConnection()
    config_file = 'config.json'
    settings = loadConfig(config_file)
    if settings is None:
        print('Config File, {}, is empty. Run gui_config.py'.format(config_file))
        exit(9)

    baseURL = 'http://{}:5000/hivedata/'.format(settings['host'])

    print('configuring probes')
    for probe in settings['probes']:
        GPIO.setup(probe['DHTPin'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True:
      #  try:
            tmp_probes = []
            for probe in settings['probes']:
                print("Checking probe, {}".format(probe['DHTModel']))
                RHW, TW = humidity, temperature = \
                    Adafruit_DHT.read_retry(probe['DHTModel'], probe['DHTPin'])
                tmp_probes.append({'model': probe['DHTModel'],
                                   'outdoor': probe['outdoor'],
                                   'humidity': RHW, 'temperature': TW})
            content = {'hive': {'id': settings['hiveId']},
                       'probes': tmp_probes}

    #        if network:
    #            html = requests.post(baseURL, json=content)
    #        else:
            if settings['DataStore'] == 0:
               writeData(settings['filename'], content)

            sleep(int(settings['delay']))
      #  except:
      #      print('Error')


if __name__ == '__main__':
    main()
