import os
import json
import logging

logger = logging.getLogger(__name__)

dhtTypes = [{'None': 0}, {'DHT11': 11}, {'DHT22': 22}, {'AM2302': 2302}]
dhtTypesValues = [0, 11, 22, 2302]

def get_probe_types():
    return dhtTypesValues


def load_config(file_name):
    data = {'host': 'localhost', 'port': 5000, 'dataStore': 0, 'delay': 300,
            'hiveId': 1, 'filename': 'hivedata.csv', 'probes': []}

    config_exists = os.path.exists(file_name)

    if config_exists:
        with open(file_name) as data_file:
            logger.debug("Successfully open config file, {}".
                         format(file_name))
            data = json.load(data_file)
    else:
        logger.debug("Failed to open config file, {}".format(file_name))

    return data


def write_config(data, file_name):
    logger.debug("Writing config file, {}".format(file_name))
    with open(file_name, "w") as data_file:
        json.dump(data, data_file)
