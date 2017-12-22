import os
import json
import logging
from config import *

logger = logging.getLogger('cmd_config')
logging.basicConfig(filename='bee_config.log',level=logging.INFO)
DATA_DIR=os.environ.get("DATA_DIR", os.path.dirname(
    os.path.realpath(__file__)))


def prompt(message, errormessage, isvalid, default_value=None):
    """Prompt for input given a message and return that value after verifying the input.

    Keyword arguments:
    message -- the message to display when asking the user for the value
    errormessage -- the message to display when the value fails validation
    isvalid -- a function that returns True if the value given by the user is valid
    """
    res = None
    while res is None:
        res = input(str(message)+': ')
        if res is '' and default_value is not None:
            return default_value

        if not isvalid(res):
            print(str(errormessage))
            res = None
    return res


def print_help():
    print("This script is to complete the configuration of your bee pi setup.")
    print("If you prefer, you may manually update the config file, "
          "'config.json'")
    print("\n")
    cont_script = input("Update configuration file (y/n) (default=n)?")
    if cont_script is None or cont_script.upper() == 'N':
        return False
    else:
        return True


def get_settings(settings):
    settings['hiveId'] = prompt(
        message="Enter an unique hive identifier. Current value is {}".
            format(settings['hiveId']),
        errormessage="Enter a valid, positive integer. If you have more than "
                     "one hive these must be unique",
        isvalid=lambda v : int(v),
        default_value=settings['hiveId']
    )

    settings['delay'] =  prompt(
        message="Enter delay (in seconds) for getting probe readings. Default "
                "is 900 seconds (15 minutes). Current settings is {}".
                format(settings['delay']),
        errormessage="Enter a valid, positive integer. More frequent checks "
                     "will result in more data",
        isvalid=lambda v: int(v),
        default_value=settings['delay']
    )
    settings['dataStore'] = prompt(
        message="Use local=0 or API=1 for storing data? Current setting is {}".
                format(settings['dataStore']),
        errormessage="Valid response is 0 or 1",
        isvalid=lambda v: v in [0,1],
        default_value=settings['dataStore']
    )

    if  settings['dataStore'] == 1:
        settings['host'] = prompt(
            message="Enter the server name to connect to. Current setting is "
                    "{}".format(settings['host']),
            errormessage="Name of the server is required. It may be localhost",
            isvalid=lambda v: True,
            default_value=settings['host']
        )

    for probe in settings['probes']:
        probe['model'] = prompt(
            message="Enter the DHT Model for probe on pin, {}. Value is {}".
                    format(probe['pin'], probe['model']),
            errormessage="Valid values are {}".format(getProbeTypes()),
            isvalid=lambda v: v in getProbeTypes(),
            default_value=probe['model']
        )

        outdoor = prompt(
            message="Is the probe outside the hive (Y/N)? Default=Y",
            errormessage="Valid values are Y or N",
            isvalid=lambda v: v.upper() in ('Y','N'),
            default_value='Y'
        )
        if outdoor == "N":
            probe['outdoor'] = "False"
        else:
            probe['outdoor'] = "True"

    return settings


def main():
    filename = os.path.join(DATA_DIR, 'config.json')
    data = loadConfig(filename, logger)
    if print_help():
        writeConfig(get_settings(data), filename, logger)


if __name__ == '__main__':
    main()