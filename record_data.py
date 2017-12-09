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
GPIO.setup(DHTpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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


def createConfig(fileName):
    data = {'host': 'localhost', 'DHTPin': 4, 'DHTModel': 0,
            'DataStore': 0, 'delay': 300, 'hiveId': 1,
            'filename': 'beedata.csv'}
    with open(fileName, "w") as data_file:
        json.dump(data, data_file)


def loadConfig(file_name):
    config_is_new = not os.path.exists(file_name)
    global settings

    if config_is_new:
        createConfig(file_name)

    with open(file_name) as data_file:
        settings = json.load(data_file)

def writeData(hiveData):
    with open(settings['filename'], 'a') as data_file:
        line = '{},{},{},{}\n'.format(hiveData['hive']['id'], 
               datetime.utcnow(), hiveData['temperature'],
               hiveData['humidity'])
        data_file.write(line)


def postDB(hiveData):
    if settings['DataStore'] == 'File':
        writeData(hiveData)


def main():
    print('starting...')
    network = checkForNetworkConnection()

    loadConfig('config.json')

    baseURL = 'http://{}:5000/hivedata/'.format(settings['host'])

    while True:
    #    try:
            RHW, TW = humidity, temperature = \
                Adafruit_DHT.read_retry(settings['DHTModel'], settings['DHTPin'])
            content = {'hive': {'id': settings['hiveId']}, 'humidity': RHW,
                       'temperature': TW}

    #        if network:
    #            html = requests.post(baseURL, json=content)
    #        else:
            postDB(content)

            sleep(int(settings['delay']))
    #    except:
    #        print('Error')


if __name__ == '__main__':
    main()
