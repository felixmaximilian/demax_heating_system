# -*- coding: utf-8-*-
from demax_backend.services.sensors.simulation_service import TemperatureSimulator as temperature_sim

def test_can_get_temperature_from_new_sensor():
    sensor_id = "0"
    temperature = 100.
    new_temperature = 99.
    temperature_sim.mock_sensor_dir()
    temperature_sim.create_sensor(sensor_id=sensor_id, temperature=temperature)

    sensor = temperature_sim.get_sensor(sensor_id)
    assert sensor.get_temperature() == temperature

    temperature_sim.set_temperature_on_sensor(sensor_id, new_temperature)

    assert sensor.get_temperature() == new_temperature
