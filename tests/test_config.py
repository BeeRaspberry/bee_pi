from config import get_probe_types, write_config, load_config


def test_write_config():
    settings = { "host": "localhost", "probes": [
        {"pin": 4, "sensor": 22, "outdoor": "False"}, {"pin": 21, "sensor": 11,
                                                       "outdoor": "True"}],
                 "dataStore": 0, "delay": 300, "hiveId": 1,
                 "filename": "hivedata.csv"}
    write_config(settings, 'tempfile.json')

    file_settings = load_config('tempfile.json')
    assert settings == file_settings


def test_get_probe_types():
    assert get_probe_types() == [0, 11, 22, 2302]
