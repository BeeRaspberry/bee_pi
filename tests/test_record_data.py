import os
import unittest
from datetime import datetime

from record_data import (check_for_network_connection,
                         write_data)


class TestTestClass(unittest.TestCase):
    def test_check_network_connection(self):
        network_connected = check_for_network_connection()
        self.assertEqual(network_connected, True)

    def test_write_data(self):
        DATA_DIR = os.environ.get("DATA_DIR", os.path.dirname(
            os.path.realpath(__file__)))
        filename = os.path.join(DATA_DIR, '..', 'tempfile')
        try:
            os.remove(filename)
        except Exception:
            pass

        date_time = datetime.utcnow().__str__()
        data = {'hive': {'id': 1},
                'probes': [
                    {'sensor': 11, 'humidity': 22.0, 'outdoor': 'True',
                     'temperature': 18.0},
                    {'sensor': 22, 'humidity': 35.599998474121094,
                     'outdoor': 'False',
                     'temperature': 19.799999237060547}],
                    'dateCreated': date_time}
        write_data('tempfile', data)
        probe = data['probes'][0]
        line = '{},{},{},{},{:.3f},{:.3f}\n'. \
            format(data['hive']['id'], data['dateCreated'], probe['sensor'],
                   probe['outdoor'], probe['temperature'], probe['humidity'])

        with open(filename) as f:
            content = f.readlines()

        self.assertEqual(line, content[0])
