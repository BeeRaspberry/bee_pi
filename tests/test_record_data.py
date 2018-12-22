import json
from datetime import datetime

from bee_pi.record_data import (check_for_network_connection, write_data)


def test_check_network_connection():
    network_connected = check_for_network_connection()
    assert network_connected is True


# TODO: Need to get sample data from PI
#def test_write_data():
#    data = {
#        "host": "localhost",
#        "probes": [{
#            "pin": 4,
#            "sensor": 22,
#            "outdoor": "False"
#        }, {
#            "pin": 21,
#            "sensor": 11,
#            "outdoor": "True"
#        }],
#        "dataStore": 0,
#        "delay": 300,
#        "hive": 1,
#        'dateCreated': datetime.utcnow().__str__(),
#        "filename": "hivedata.csv"
#    }

#    write_data('temp.dat', data)
#    with open('temp.dat') as data_file:
#        file_data = json.load(data_file)
#    assert data == file_data
