import json
import os

def loadConfig(file_name):
    global data, original_data

    data = {'host': 'localhost', 'DataStore': 0, 'delay': 300, 'hiveId': 1,
            'filename': 'beedata.csv', 'probes': []}

    config_exists = os.path.exists(file_name)

    if config_exists:
        with open(file_name) as data_file:
            data = json.load(data_file)
#    else:
#        data['probes'] = find()

    original_data = data


def writeConfig(fileName):
    with open(fileName, "w") as data_file:
        json.dump(data, data_file)