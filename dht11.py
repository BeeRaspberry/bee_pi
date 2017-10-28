# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import json
import requests
import logging
from urllib.request import urlopen



DEBUG = 1
# Setup the pins we are connect to
RCpin = 24
DHTpin = 4

#Setup our API and delay
myAPI = "***Insert Your API CODE HERE***"
myDelay = 900 #how many seconds between posting data

GPIO.setmode(GPIO.BCM)
GPIO.setup(DHTpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


logger = logging.getLogger('dht11')


def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    #Convert from Celius to Farenheit
    TWF = 9/5*TW+32
    # return dict
    return [RHW, TW, TWF]


def load_config(file_name):
    with open(file_name) as data_file:
        data = json.load(data_file)
        return data
    
def main():
    print ('starting...')
    settings = load_config('config.json')

    baseURL = 'http://{}:5000/hivedata/'.format(settings['host'])


    while True:
        try:
            RHW, TW, TWF = getSensorData()
            content={'hive':{'id': settings['hiveId']}, 'humidity': RHW,
                'temperature': TW}

            html = requests.post(baseURL, json=content)

            sleep(int(settings['delay']))
        except:
            print ('exiting.')
            break

if __name__ == '__main__':
    main()
