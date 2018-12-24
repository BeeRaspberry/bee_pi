# Import all the libraries we need to run
from time import sleep
from config import *

from datetime import datetime
import platform
import netifaces
import requests

# TODO: Need to run this on a PI.
if 'armv' in platform.machine():
    import Adafruit_DHT
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

logger = logging.getLogger('record_data')
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
DATA_DIR = os.environ.get("DATA_DIR", os.path.dirname(
    os.path.realpath(__file__)))


def check_for_network_connection():
    network_connected = False
    for interface in netifaces.interfaces():
        addr = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addr and \
                addr[netifaces.AF_INET][0]['addr'] != '127.0.0.1':
            network_connected = True
    return network_connected


def write_data(filename, hive_data):
    filename = os.path.join(DATA_DIR, filename)

    with open(filename, 'a') as data_file:
        logger.debug("Writing to data to file, {}".format(filename))
        for probe in hive_data['probes']:
            line = '{},{},{},{},{:.3f},{:.3f}\n'.\
                format(hive_data['hive']['id'], hive_data['dateCreated'],
                       probe['sensor'], probe['outdoor'],
                       probe['temperature'], probe['humidity'])
            data_file.write(line)


def main():
    logger.debug('starting collecting data')
    config_file = os.path.join(DATA_DIR, 'config.json')

    settings = load_config(config_file, logger)
    if settings is None:
        logger.error('Config File, {}, is empty. Run cmd_config.py'.
                     format(config_file))
        exit(9)

    base_url = 'http://{}:{}/hivedata/'.format(settings['host'],
                                               settings['port'])

    logger.debug('configuring probes')
    for probe in settings['probes']:
        GPIO.setup(probe['pin'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    network_connected = check_for_network_connection()

    while True:
        tmp_probes = []
        for probe in settings['probes']:
            logger.debug("Checking probe, {}".format(probe['sensor']))
            rhw, tw = Adafruit_DHT.read_retry(probe['sensor'], probe['pin'])
            tmp_probes.append({'sensor': probe['sensor'],
                               'outdoor': probe['outdoor'],
                               'humidity': rhw, 'temperature': tw})
            content = {'hive': {'id': settings['hiveId']}, 'dateCreated':
                       datetime.utcnow().__str__(), 'probes': tmp_probes}

            if network_connected and settings['dataStore'] == 1:
                try:
                    response = requests.post(base_url, json=content,
                                             timeout=30.0)
                    if response.status_code != requests.codes.ok:
                        logger.warning('Invalid Response: code: {}, '
                                       'response: {}'.format(
                                        response.status_code,
                                        response.json()['message']))
                except requests.exceptions.RequestException as e:
                    logger.warning('Connection Error: {}'.format(e))
                    logger.warning('Connection Error. Writing data locally')
                    write_data(settings['filename'], content)
            else:
                write_data(settings['filename'], content)

            sleep(int(settings['delay']))


if __name__ == '__main__':
    main()
