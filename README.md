# bee_pi
[![Build Status](https://travis-ci.org/BeeRaspberry/bee_pi.svg?branch=master)](https://travis-ci.org/BeeRaspberry/bee_pi)
[![CircleCI](https://circleci.com/gh/BeeRaspberry/bee_pi.svg?style=svg)](https://circleci.com/gh/BeeRaspberry/bee_pi)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0dd7ae717fb34eebaae1fd65b40ae881)](https://app.codacy.com/app/erikdeirdre/bee_pi?utm_source=github.com&utm_medium=referral&utm_content=BeeRaspberry/bee_pi&utm_campaign=Badge_Grade_Dashboard)
[![Coverage Status](https://coveralls.io/repos/github/BeeRaspberry/bee_pi/badge.svg)](https://coveralls.io/github/BeeRaspberry/bee_pi)
[![codecov](https://codecov.io/gh/BeeRaspberry/bee_pi/branch/master/graph/badge.svg)](https://codecov.io/gh/BeeRaspberry/bee_pi)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/BeeRaspberry/bee_pi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BeeRaspberry/bee_pi/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/BeeRaspberry/bee_pi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/BeeRaspberry/bee_pi/context:python)

Bee PI is one component of a Python-based application for monitoring a bee hive using a Raspberry PI.

This project records temperature and humidity into a csv-based file, or via API. 

The module is intended to be as close as possible to plug-and-play. 

Included code scans for probes so user doesn't have to setup the PI with the ports, and models (DHT11, DHT22, etc.) automatically.

## Installation
Installation is a three step process.

- download [installation package](../../releases/download/release-0.1/files.tgz)
```bash
wget https://github.com/BeeRaspberry/bee_pi/releases/download/release-0.1/files.tgz
```
- uncompress file
```bash
tar -xzvf files.tgz
```
- run **install.sh**
```bash
sudo ./install.sh
```

### Main Components

This repo's main components are:
- **config.json**
- **find_probes.py**
- **gui_config.py**
- **cmd_config**
- **record_data.py**
- **install.sh**

#### config.json

This is the configuration file used by record_data.py to determine what probes exist, and their settings. The file also instructions the python script to write the results locally, or post to a Rest API.

```json
{
	"host": "localhost",
	"probes": [{
		"pin": 4,
		"sensor": 22,
		"outdoor": "False"
	},{
		"pin": 21,
		"sensor": 11,
		"outdoor": "True"	
	}],
	"dataStore": 0,
	"delay": 300,
	"hiveId": 1,
	"filename": "hivedata.csv"
}
```
The file is built primarily via **find_probes.py** which finds the probes, and sets the config file to write locally.

**gui_config.py** supplements the process by allowing the user to make changes to the file without knowing geek stuff. **NOTE:** I had problems installing the wx.Python module on my PI resulting in **cmd_config.py**.

**cmd_config.py** is a command line version of **gui_config.py**.

**install.sh** installs the required components. Steps include:
- creates the virtualenv environment
- runs `find_probes.py`
- executes `cmd_config.py`
- configures `systemd` so the process runs as a service

##### config.json variable explained
- `host` refers to the API host when the module is running in API mode.
- `port` refers to the API port when the module is running in API mode.
- `probes` is an array of probes (thermometers, and humidity; currently). Within the array are:
  - `pin` refers to the Raspberry PI pin the probe is attached to.
  - `sensor` indicates the probe model (currently DHT11, DHT22, AM2302)
  - `outdoor` indicates the location of the probe.
- `dataStore` informs the system the data is written to a file or an API-based.
- `delay` is the time in seconds for the process to wait between probe readings.
- `hiveId` is a unique identifier for those who have multiple hives.
- `filename` is the file name used to store the data when the datastore is `0`.

## Work Flow
The work flow is simple.
1. read the configuraton file
2. check the defined probes for values
3. record data
   1. transmit data if API enabled AND network available
   2. store data locally if API is disabled, network isn't available, or API call failed.
4. sleep for the configured time; repeat, starting with step 2.

## Installation Troubleshooting

| Problem | Solution
| --- | ---
| N/A | N/A
