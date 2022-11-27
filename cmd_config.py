import os
import logging
from config import (get_probe_types, load_config, write_config)
logger = logging.getLogger('cmd_config')
logging.basicConfig(level=logging.INFO)
DATA_DIR = os.getenv("DATA_DIR", os.path.dirname(os.path.realpath(__file__)))


def prompt(message, error_message, isvalid, default_value=None):
    res = None
    while res is None:
        res = input(str(message)+': ')
        if res == '' and default_value is not None:
            return default_value

        if not isvalid(res):
            print(str(error_message))
            res = None
    return res


def print_help():
    print("This script is to complete the configuration of your bee pi "
          "setup.")
    print("If you prefer, you may manually update the config file, "
          "'config.json'")
    print("\n")
    try:
        cont_script = input("Update configuration file (y/n) (default=n)?")
        if cont_script.upper() == 'Y':
            return True
        else:
            return False
    except EOFError:
        return False


def get_settings(settings):
    settings['hiveId'] = int(prompt(
        message="Enter an unique hive identifier. Current value is {}".
                format(settings['hiveId']),
        error_message="Enter a valid, positive integer. If you have more than "
                     "one hive these must be unique",
        isvalid=lambda v: int(v),
        default_value=settings['hiveId']
    ))

    settings['delay'] = int(prompt(
        message="Enter delay (in seconds) for getting probe readings. Default "
                "is 900 seconds (15 minutes). Current settings is {}".
                format(settings['delay']),
        error_message="Enter a valid, positive integer. More frequent checks "
                     "will result in more data",
        isvalid=lambda v: int(v),
        default_value=settings['delay']
    ))
    settings['dataStore'] = int(prompt(
        message="Use local=0 or API=1 for storing data? Current setting is {}".
                format(settings['dataStore']),
        error_message="Valid response is 0 or 1",
        isvalid=lambda v: v in [0, 1],
        default_value=settings['dataStore']
    ))

    if settings['dataStore'] == 1:
        settings['host'] = prompt(
            message="Enter the server name to connect to. Current setting is "
                    "{}".format(settings['host']),
            error_message="Name of the server is required. It may be localhost",
            isvalid=lambda v: True,
            default_value=settings['host']
        )
        settings['port'] = prompt(
            message="Enter the Port to connect to. Current setting is "
                    "{}".format(settings['port']),
            error_message="Port is required.",
            isvalid=lambda v: True,
            default_value=settings['port']
        )
    for probe in settings['probes']:
        probe['sensor'] = prompt(
            message="Enter the DHT Model for probe on pin, {}. Value is {}".
                    format(probe['pin'], probe['sensor']),
            error_message="Valid values are {}".format(get_probe_types()),
            isvalid=lambda v: v in get_probe_types(),
            default_value=probe['sensor']
        )

        outdoor = prompt(
            message="Is the probe outside the hive (Y/N)? Default=Y",
            error_message="Valid values are Y or N",
            isvalid=lambda v: v.upper() in ('Y', 'N'),
            default_value='Y'
        )
        if outdoor == "N":
            probe['outdoor'] = "False"
        else:
            probe['outdoor'] = "True"

    return settings


def check_for_probes(settings):
    if 'probes' in settings and len(settings['probes']) > 0:
        return True

    return False


def main():
    filename = os.getenv("CONFIG_FILE", 'config.json')
    data = load_config(filename)
    if print_help():
        if check_for_probes(data):
            write_config(get_settings(data), filename)
        else:
            print("No probes found. Run 'find_probes.py' to find them.")


if __name__ == '__main__':
    main()
