import json
import os

dhtTypes = [{'None': 0}, {'DHT11':11}, {'DHT22':22}, {'AM2302':2302}]
dhtTypesValues = [0,11,22,2302]

def getProbeTypes():
    return dhtTypesValues


def loadConfig(file_name, logger):
    data = {'host': 'localhost', 'dataStore': 0, 'delay': 300, 'hiveId': 1,
            'filename': 'beedata.csv', 'probes': []}

    config_exists = os.path.exists(file_name)

    if config_exists:
        with open(file_name) as data_file:
            logger.debug("Successfully open config file, {}".format(file_name))
            data = json.load(data_file)
    else:
        logger.debug("Failed to open config file, {}".format(file_name))

    return data


def writeConfig(data, fileName, logger):
    logger.debug("Writing config file, {}".format(fileName))
    with open(fileName, "w") as data_file:
        json.dump(data, data_file)