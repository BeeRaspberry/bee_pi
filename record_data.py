# Import all the libraries we need to run
import sys
import os
from time import sleep
from datetime import datetime
import netifaces
import json
import requests
import logging
from urllib.request import urlopen
import Adafruit_DHT
import RPi.GPIO as GPIO
from config import *


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = logging.getLogger('record_data')
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
DATA_DIR=os.environ.get("DATA_DIR", os.path.dirname(
    os.path.realpath(__file__)))


def checkForNetworkConnection():
    networkConnected = False
    interfaces = netifaces.interfaces()
    for interface in netifaces.interfaces():
        addr = netifaces.ifaddresses(interface)
        if addr[netifaces.AF_INET] != '' and \
                addr[netifaces.AF_INET][0]['addr'] != '127.0.0.1':
            networkConnected = True
    return networkConnected


def writeData(filename, hiveData):
    filename = os.path.join(DATA_DIR, filename)

    with open(filename, 'a') as data_file:
        logger.debug("Writing to data to file, {}".format(filename))
        for probe in hiveData['probes']:
            line = '{},{},{},{},{},{}\n'.format(hiveData['hive']['id'],
                datetime.utcnow(), probe['model'], probe['outdoor'],
                probe['temperature'], probe['humidity'])
            data_file.write(line)


def main():
    logger.debug('starting collecting data')
#    network = checkForNetworkConnection()
    config_file = os.path.join(DATA_DIR, 'config.json')

    settings = loadConfig(config_file, logger)
    if settings is None:
        logger.error('Config File, {}, is empty. Run cmd_config.py'.
                     format(config_file))
        exit(9)

    baseURL = 'http://{}:5000/hivedata/'.format(settings['host'])

    logger.debug('configuring probes')
    for probe in settings['probes']:
        GPIO.setup(probe['pin'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    networkConnected = checkForNetworkConnection()
    
    while True:
      #  try:
            tmp_probes = []
            for probe in settings['probes']:
                logger.debug("Checking probe, {}".format(probe['sensor']))
                RHW, TW = humidity, temperature = \
                    Adafruit_DHT.read_retry(probe['sensor'], probe['pin'])
                tmp_probes.append({'model': probe['sensor'],
                                   'outdoor': probe['outdoor'],
                                   'humidity': RHW, 'temperature': TW})
            content = {'hive': {'id': settings['hiveId']},
                       'probes': tmp_probes}

            if networkConnected and settings['dataStore'] == 1:
                try:
                    html = requests.post(baseURL, json=content)
                except ConnectionError as e:
                    logger.error('Connection Error: {}'.format(config_file))
                    if e.errno == 111:
                        logger.error('Connection Refused. Switch to local writing')
                        settings['dataSource'] = 0
            else:
                writeData(settings['filename'], content)

            sleep(int(settings['delay']))
      #  except:
      #      print('Error')


if __name__ == '__main__':
    main()
