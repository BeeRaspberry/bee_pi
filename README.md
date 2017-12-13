# bee_pi

Bee PI is one component of a Python-based application for monitoring a bee hive using a Raspberry PI.

This project records temperature and humidity into a csv-based file, or via API. 

The module is intended to be as close as possible to plug-and-play. 

Included code scans for probes so user doesn't have to setup the PI with the ports, and models (DHT11, DHT22, etc.) automatically.

A GUI program exists to help with the configuration. The UI allows the user to specify a remote host for API calls, and whether a probe is inside or outside the hive.

### Main Components

This repo's main components are **config.json**, **find_probes.py**, **gui_config.py**, and **record_data.py**.

#### config.json

This is the configuration file used by record_data.py to determine what probes exist, and their settings. The file also instructions the python script to write the results locally, or post to a Rest API.

```json
{
	"host": "localhost",
	"probes": [{
		"DHTPin": 4,
		"DHTModel": 22,
		"outdoor": "False"
	},{
		"DHTPin": 21,
		"DHTModel": 11,
		"outdoor": "True"	
	}],
	"DataStore": 0,
	"delay": 300,
	"hiveId": 1,
	"filename": "beedata.csv"
}
```
The file is built primarily via **find_probes.py** which finds the probes, and setting the config file to write locally.

**gui_config.py** supplements the process by allowing the user to make changes to the file without knowing geek stuff.

##### config.json variable explanation
- `host` refers to the API host when the module is running in API mode.
- `probes` is an array of probes (thermometers, and humidity; currently). Within the array are:
  - `DHTPin` refers to the Raspberry PI pin the probe is attached to.
  - `DHTModel` indicates the probe model (currently DHT11, DHT22, AM2302)
  - `outdoor` indicates the location of the probe.
- `DataStore` informs the system the data is written to a file or an API-based.
- `delay` is the time in seconds for the process to wait between probe readings.
- `hiveId` is a unique identifier for those who have multiple hives.
- `filename` is the file name used to store the data when the datastore is `0`.