from bee_pi.config import *

logger = logging.getLogger('cmd_config')
logging.basicConfig(level=logging.INFO)
DATA_DIR = os.environ.get("DATA_DIR", os.path.dirname(
    os.path.realpath(__file__)))


def prompt(message, errormessage, isvalid, default_value=None):
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
    print("This script is to complete the configuration of your bee pi "
          "setup.")
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
        isvalid=lambda v: int(v),
        default_value=settings['hiveId']
    )

    settings['delay'] = prompt(
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
        isvalid=lambda v: v in [0, 1],
        default_value=settings['dataStore']
    )

    if settings['dataStore'] == 1:
        settings['host'] = prompt(
            message="Enter the server name to connect to. Current setting is "
                    "{}".format(settings['host']),
            errormessage="Name of the server is required. It may be localhost",
            isvalid=lambda v: True,
            default_value=settings['host']
        )
        settings['port'] = prompt(
            message="Enter the Port to connect to. Current setting is "
                    "{}".format(settings['port']),
            errormessage="Port is required.",
            isvalid=lambda v: True,
            default_value=settings['port']
        )
    for probe in settings['probes']:
        probe['sensor'] = prompt(
            message="Enter the DHT Model for probe on pin, {}. Value is {}".
                    format(probe['pin'], probe['sensor']),
            errormessage="Valid values are {}".format(get_probe_types()),
            isvalid=lambda v: v in get_probe_types(),
            default_value=probe['sensor']
        )

        outdoor = prompt(
            message="Is the probe outside the hive (Y/N)? Default=Y",
            errormessage="Valid values are Y or N",
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
    filename = os.path.join(DATA_DIR, 'config.json')
    data = load_config(filename)
    if print_help():
        if check_for_probes(data):
            write_config(get_settings(data), filename, logger)
        else:
            print("No probes found. Run 'find_probes.py' to find them.")


if __name__ == '__main__':
    main()
