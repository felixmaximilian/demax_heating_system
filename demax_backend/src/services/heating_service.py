from time import sleep

from configs import TEMPERATURE_SENSOR, SW_HYSTERESE, SW_BU_HYSTERESE, PUMPS, SO_DELTA_HYSTERESE
from services.sensors.temperature_service import DS18B20, Hysterese


def handle_heating_desired(switch_holder):
    """
    Modus fuer Vorhalten von Waerme (Warmwasser). An, zu bestimmten Zeiten an bestimmten Wochentagen und besonderen Einzeltagen (Feiertage) - active_schedule.
    Wenn:
    - BW (oben) <= BW_MAX (BW noch nicht warm genug)
    - WENN Sensor BW_oben (1) - sensor PS (4) >= BW_PS_DELTA (7) Hysterese
    DANN WECHSLER Ladepumpe (1) AN
    - Else (PS nicht warm genug):
    DANN WECHSLER Ladepumpe (1) AUS
    UND
    Wechsler Brauchwasser heizen elektrisch (4) AN
    :return:
    """
    sw_sensor = DS18B20(TEMPERATURE_SENSOR["SW_TOP"]["id"])
    sw_temperature = sw_sensor.get_temperature()
    bu_sensor = DS18B20(TEMPERATURE_SENSOR["BU_TOP"]["id"])
    bu_temperature = bu_sensor.get_temperature()
    loading_pump_relais = switch_holder.get("loading_pump")
    electrical_heating_relais = switch_holder.get("electrical_heating_service_water")

    sw_hyst = Hysterese(**SW_HYSTERESE)
    delta_hyst = Hysterese(**SW_BU_HYSTERESE)
    if sw_hyst.is_in_upper_alarm(sw_temperature):
        loading_pump_relais.set_low()
        electrical_heating_relais.set_low()
    elif sw_hyst.is_in_lower_alarm(sw_temperature):
        delta = bu_temperature - sw_temperature
        if delta_hyst.is_in_upper_alarm(delta):
            electrical_heating_relais.set_low()
            loading_pump_relais.set_high()
        elif delta_hyst.is_in_lower_alarm(delta):
            loading_pump_relais.set_low()
            electrical_heating_relais.set_high()
        # ELSE, we cannot turn on elect heating because of hystese, but Bu does not provide enough heat neither


def handle_solar_panel(switch_holder):
    sw_sensor = DS18B20(TEMPERATURE_SENSOR["SW_BOTTOM"]["id"])
    sw_temperature = sw_sensor.get_temperature()
    so_sensor = DS18B20(TEMPERATURE_SENSOR["SO_TOP"]["id"])
    so_temperature = so_sensor.get_temperature()

    true_delta = so_temperature - sw_temperature
    so_delta_hyst = Hysterese(**SO_DELTA_HYSTERESE)
    if so_delta_hyst.is_in_upper_alarm(true_delta):
        switch_holder.get("solar_pump").set_high()
    elif so_delta_hyst.is_in_lower_alarm(true_delta):
        switch_holder.get("solar_pump").set_low()


def handle_move_all_pumps(switch_holder):
    for switch_key in PUMPS:
        switch = switch_holder.get(switch_key)
        if not switch.get_state():
            switch.set_high()
            sleep(60)
            switch.set_low()
