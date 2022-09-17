import argparse
import logging
import random
from time import sleep
import sys
import fake_rpi
from apscheduler.schedulers.blocking import BlockingScheduler

from services import heating_service
from services.sensors.simulation_service import TemperatureSimulator as temperature_sim
from configs import TEMPERATURE_SENSOR, SWITCHES

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--simulation-mode",
        action="store_true",
        help="Simulate sensor values and switches instead of using the ones connected.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    # TODO: Parse Temperature IDs from config
    # config = configparser.ConfigParser()
    # config.sections()
    #
    # config.read('example.ini')
    #
    # config.sections()

    if args.simulation_mode:
        # create sensor dir and mock it in the sensor service
        temperature_sim.mock_sensor_dir()

        # setting up the sensors
        for sensor_name, sensor_config in TEMPERATURE_SENSOR.items():
            temperature_sim.create_sensor(sensor_config["id"], random.gauss(40., 10.))
        temperature_sim.start_temperature_simulation()

        # TODO export to separate
        sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
        sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO
    from services.database_service import update_temperatures, update_switches_data
    from services.actors.relais import SwitchHolder

    switch_holder = SwitchHolder(SWITCHES)
    scheduler = BlockingScheduler()

    while True:
        sleep(5)
        # TODO
        # update_modes_from_schedule_or_manual_intervention()

        # write sensor values, switch states and mode states to db
        # TODO: extract into own thread.
        # update_temperatures(TEMPERATURE_SENSOR)
        # update_switches_data(SWITCHES)

        heating_service.handle_heating_desired(switch_holder)
        heating_service.handle_solar_panel(switch_holder)

