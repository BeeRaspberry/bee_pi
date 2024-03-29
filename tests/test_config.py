import unittest
from config import (get_probe_types, write_config, load_config)


class TestConfig(unittest.TestCase):
    def test_write_config(self):
        settings = {"host": "localhost", "probes": [
            {"pin": 4, "sensor": 22, "outdoor": "False"}, {"pin": 21, "sensor": 11,
                                                       "outdoor": "True"}],
                 "dataStore": 0, "delay": 300, "hiveId": 1,
                 "filename": "hivedata.csv"}
        write_config(settings, 'tempfile.json')

# tests load_config method as well
        file_settings = load_config('tempfile.json')
        self.assertEqual(settings, file_settings)

    def test_get_probe_types(self):
        self.assertEqual(get_probe_types(), ['0', '11', '22', '2302'])
