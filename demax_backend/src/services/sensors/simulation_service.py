import logging
import os
import random
import tempfile
from os import path
from time import sleep
from threading import Thread

from services.sensors.temperature_service import DS18B20


class TemperatureSimulator(object):
    units = {"C": DS18B20.DEGREES_C, "F": DS18B20.DEGREES_F, "K": DS18B20.KELVIN}

    __TEMPERATURE_SENSOR_FORMAT__ = """9e 01 4b 46 7f ff 02 10 56 : crc=56 YES
    9e 01 4b 46 7f ff 02 10 56 t=%d
    """
    sensor_dir = tempfile.TemporaryDirectory()

    @classmethod
    def mock_sensor_dir(cls):
        cls.sensor_dir = tempfile.TemporaryDirectory()
        DS18B20.BASE_DIRECTORY = cls.sensor_dir.name

    @classmethod
    def create_sensor(cls, sensor_id: str, temperature=42.):
        sensor_path = path.join(DS18B20.BASE_DIRECTORY, DS18B20.SLAVE_PREFIX + sensor_id)
        if not path.exists(sensor_path):
            os.mkdir(sensor_path)
            with open(path.join(sensor_path, DS18B20.SLAVE_FILE), "w+") as f:
                data = cls.__TEMPERATURE_SENSOR_FORMAT__ % (temperature * 1000)
                f.write(data)

        sensors = [sensor for sensor in DS18B20.get_all_sensors() if sensor.get_id() == sensor_id]
        if not sensors:
            raise ValueError("Could not find new sensor with id %s." % sensor_id)

    @classmethod
    def set_temperature_on_sensor(cls, sensor_id, temperature):
        """Sets the temperature (in celsius) on a mocked sensor"""
        sensor_path = path.join(DS18B20.BASE_DIRECTORY, DS18B20.SLAVE_PREFIX + sensor_id)
        if not path.exists(sensor_path):
            logging.warning("No mocked sensor with id %s found. Creating file." % sensor_id)

        data = cls.__TEMPERATURE_SENSOR_FORMAT__ % (temperature * 1000)
        with open(path.join(sensor_path, DS18B20.SLAVE_FILE), "w+") as f:
            f.write(data)

        return True

    @classmethod
    def get_sensor(cls, sensor_id):
        sensors = [sensor for sensor in DS18B20.get_all_sensors() if sensor.get_id() == sensor_id]
        return sensors[0]

    @classmethod
    def start_temperature_simulation(cls):
        def task():
            # block for a moment
            i = 0
            while True:
                sleep(1)

                [cls.set_temperature_on_sensor(sensor.get_id(), random.gauss(40., 10.)) for sensor in
                 DS18B20.get_all_sensors()]
                i += 1

        thread = Thread(target=task)
        thread.start()
