# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import Adafruit_DHT

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

possible_pins = {2:[2,3,4,7,8,9,10,11,14,15,17,18,22,23,24,25,27]}
sensor_types = (Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, Adafruit_DHT.AM2302)
used_pins = []
probes=[]


def find():
    seconds = len(sensor_types) * len(possible_pins[GPIO.RPI_REVISION])
    print("starting... be patient this will take about {} seconds".format(seconds))

    for sensor in sensor_types:
        for pin in possible_pins[GPIO.RPI_REVISION]:
            if pin not in used_pins:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                h, t = Adafruit_DHT.read_retry(sensor, pin, retries=3)
                if h is not None and t is not None:
                    probes.append({'sensor': sensor, 'pin': pin, 'outdoor': False})
                    used_pins.append(pin)
                else:
                    print("Nothing found for {} on pin, {}".format(sensor,pin))

                GPIO.cleanup(pin)
    return probes


if __name__ == '__main__':
    find()
