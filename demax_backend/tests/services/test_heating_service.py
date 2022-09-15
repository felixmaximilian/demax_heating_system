import fake_rpi
import sys

sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO
import RPi.GPIO as GPIO

from demax_backend.services.actors.relais import SwitchHolder

from demax_backend.services import heating_service
from demax_backend.services.sensors.simulation_service import TemperatureSimulator as temperature_simulator
from demax_backend.configs import TEMPERATURE_SENSOR, SWITCHES
import pytest

service_water_change_testdata = [
    pytest.param(22., 24., GPIO.LOW, GPIO.HIGH, id="a"),
    pytest.param(22., 30., GPIO.HIGH, GPIO.LOW, id="c"),
    pytest.param(44., 52., GPIO.LOW, GPIO.LOW, id="d"),
]


@pytest.fixture()
def switch_holder():
    return SwitchHolder(SWITCHES)


@pytest.mark.parametrize(
    "sw_top_temperature, bu_top_temperature, expected_loading_pump_state, expected_electrical_heating_state",
    service_water_change_testdata)
def test_low_service_water_temperature_expect_change(sw_top_temperature, bu_top_temperature,
                                                     expected_loading_pump_state,
                                                     expected_electrical_heating_state, mocker, switch_holder):
    temperature_simulator.mock_sensor_dir()
    spy = mocker.spy(GPIO, "output")
    # Given
    temperature_simulator.create_sensor(TEMPERATURE_SENSOR["SW_TOP"]["id"], sw_top_temperature)
    temperature_simulator.create_sensor(TEMPERATURE_SENSOR["BU_TOP"]["id"], bu_top_temperature)

    # When
    heating_service.handle_heating_desired(switch_holder)

    # Then
    spy.assert_any_call(SWITCHES["loading_pump"]["gpiopin"], expected_loading_pump_state)
    spy.assert_any_call(SWITCHES["electrical_heating_service_water"]["gpiopin"], expected_electrical_heating_state)


expect_no_change_testdata = [
    pytest.param(42.5, 50., id="In max heating hysterese."),
    pytest.param(22., 29., id="In delta hysterese, low temperature"),
    pytest.param(43., 49., id="In delta hysterese, high temperature")
]


@pytest.mark.parametrize(
    "sw_top_temperature, bu_top_temperature",
    expect_no_change_testdata)
def test_low_service_water_temperature_expect_no_action(sw_top_temperature, bu_top_temperature, mocker, switch_holder):
    temperature_simulator.mock_sensor_dir()
    spy = mocker.spy(GPIO, "output")
    # Given
    temperature_simulator.create_sensor(TEMPERATURE_SENSOR["SW_TOP"]["id"], sw_top_temperature)
    temperature_simulator.create_sensor(TEMPERATURE_SENSOR["BU_TOP"]["id"], bu_top_temperature)

    # When
    heating_service.handle_heating_desired(switch_holder)

    # Then
    spy.assert_not_called()


solar_panel_change_testdata = [
    pytest.param(30., 20., GPIO.HIGH, id="solar delivers excess heat"),
    pytest.param(30., 40., GPIO.LOW, id="solar is colder than service water"),
]

@pytest.mark.parametrize(
    "solar_panel_temperature, sw_bottom_temperature, expected_solar_pump_state",
    solar_panel_change_testdata)
def test_solar_panel_with_change(solar_panel_temperature, sw_bottom_temperature,
                                 expected_solar_pump_state, mocker, switch_holder):
    temperature_simulator.mock_sensor_dir()
    spy = mocker.spy(GPIO, "output")
    # Given
    temperature_simulator.create_sensor(TEMPERATURE_SENSOR["SO_TOP"]["id"], solar_panel_temperature)
    temperature_simulator.create_sensor(TEMPERATURE_SENSOR["SW_BOTTOM"]["id"], sw_bottom_temperature)

    # When
    heating_service.handle_solar_panel(switch_holder)

    # Then
    spy.assert_any_call(SWITCHES["solar_pump"]["gpiopin"], expected_solar_pump_state)


expect_no_change_testdata = [
    pytest.param(42.5, 50., id="In max heating hysterese."),
    pytest.param(22., 29., id="In delta hysterese, low temperature"),
    pytest.param(43., 49., id="In delta hysterese, high temperature")
]
