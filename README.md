# bee_pi
![](https://github.com/BeeRaspberry/bee_pi/workflows/build_and_package/badge.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cffc88d664b84c80ac3f9b2b3b6f53aa)](https://www.codacy.com/gh/BeeRaspberry/bee_pi/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=BeeRaspberry/bee_pi&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/cffc88d664b84c80ac3f9b2b3b6f53aa)](https://www.codacy.com/gh/BeeRaspberry/bee_pi/dashboard?utm_source=github.com&utm_medium=referral&utm_content=BeeRaspberry/bee_pi&utm_campaign=Badge_Coverage)

Bee PI is one component of a Python-based application for monitoring a bee hive using a Raspberry PI.

This project records temperature and humidity into a csv-based file, or via API. 

The module is intended to be as close as possible to plug-and-play. 

Included code scans for probes so user doesn't have to setup the PI with the ports, and models (DHT11, DHT22, etc.) automatically.

## Installation
Installation is a three step process.

-   download [installation package](../../releases/download/release-0.1/files.tgz)
```bash
wget https://github.com/BeeRaspberry/bee_pi/releases/download/release-0.1/files.tgz
```
-   uncompress file
```bash
tar -xzvf files.tgz
```
-   run **install.sh**
```bash
sudo `pwd`/install.sh
```

"`pwd`" is required to capture the current working directory. Otherwise, the script won't work. 
### Main Components

This repo's main components are:
-   **config.json**
-   **find_probes.py**
-   **cmd_config**
-   **record_data.py**
-   **install.sh**

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

**cmd_config.py** is interactive script to modify the config file.

**install.sh** installs the required components. Steps include:
-   creates the virtualenv environment
-   runs `find_probes.py`
-   executes `cmd_config.py`
-   configures `systemd` so the process runs as a service
 
##### config.json variable explained
-   `host` refers to the API host when the module is running in API mode.

-   `port` refers to the API port when the module is running in API mode.

-   `probes` is an array of probes (thermometers, and humidity; currently). Within the array are:
    -   `pin` refers to the Raspberry PI pin the probe is attached to.
    -   `sensor` indicates the probe model (currently DHT11, DHT22, AM2302)
    -   `outdoor` indicates the location of the probe.
    
-   `dataStore` 

-   `delay` is the time in seconds for the process to wait between probe readings.

-   `hiveId` is a unique identifier for those who have multiple hives.

-   `filename` is the file name used to store the data when the datastore is `0`.

## Work Flow
The work flow is simple.
1. read the configuration file
2. check the defined probes for values
3. record data
   1. transmit data if API enabled AND network available
   2. store data locally if API is disabled, network isn't available, or API call failed.
4. sleep for the configured time; repeat, starting with step 2.

## Installation Troubleshooting

| Problem | Solution |
| ---     | ---      |
| N/A     | N/A      |
