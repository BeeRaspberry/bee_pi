from config import get_probe_types, write_config, load_config


def test_write_config():
    settings = {'hiveId': 123, 'delay': 30, 'dataStore': 0,
                'host': 'localhost', 'port': 1280,
                'probes': [{'sensor': 1, 'outdoor': 'Y'}]}
    write_config(settings, 'tempfile.json')

    file_settings = load_config('tempfile.json')
    assert settings == file_settings


def test_get_probe_types():
    assert get_probe_types() == [0, 11, 22, 2302]
