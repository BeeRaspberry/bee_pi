# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import netifaces
import json
import requests
import logging
import sqlite3
from urllib.request import urlopen


DEBUG = 1
# Setup the pins we are connect to
RCpin = 24
DHTpin = 4

#Setup our API and delay
myAPI = "***Insert Your API CODE HERE***"
conn = None

GPIO.setmode(GPIO.BCM)
GPIO.setup(DHTpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


logger = logging.getLogger('dht11')


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
		

def createConfig(filename):
	print('create config')
	

def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)

    # return dict
    return [RHW, TW]


def loadConfig(file_name):
	config_is_new = not os.path.exists(file_name)
	
	if config_is_new:
		createConfig(file_name)
		
	with open(file_name) as data_file:
		data = json.load(data_file)
		return data
   
   
def postDB(hiveData):
	
	print(hiveData)
	
	 
def main():
    print ('starting...')
    network = checkForNetworkConnection()

    settings = loadConfig('config.bak')
    
    baseURL = 'http://{}:5000/hivedata/'.format(settings['host'])


    while True:
        try:
            RHW, TW = getSensorData()
            content={'hive':{'id': settings['hiveId']}, 'humidity': RHW,
                'temperature': TW}

            if network:
			    html = requests.post(baseURL, json=content)
            else:
			    postDB(content)

            sleep(int(settings['delay']))
        except:
            print ('Error')
           

if __name__ == '__main__':
    main()
