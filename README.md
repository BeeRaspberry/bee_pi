# bee_pi

Bee PI is one component of a Python-based application for monitoring a bee hive using a Raspberry PI.

This project records temperature and humidity into a csv-based file, or via API. 

The module is intended to be as close as possible to plug-and-play. 

Included code scans for probes so user doesn't have to setup the PI with the ports, and models (DHT11, DHT22, etc.) automatically.

A GUI program exists to help with the configuration. The UI allows the user to specify a remote host for API calls, and whether a probe is inside or outside the hive.