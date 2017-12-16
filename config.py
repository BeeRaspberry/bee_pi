import json
import os


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
    logger.debug("Writing config file, {}".format(filename))
    with open(fileName, "w") as data_file:
        json.dump(data, data_file)