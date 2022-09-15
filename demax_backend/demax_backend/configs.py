TEMPERATURE_SENSOR = {"SW_TOP": {"name": "Brauchwasser oben", "id": "012152634fa8"},
                      "SW_MID": {"name": "Brauchwasser mitte", "id": "012152470b34"},
                      "SW_BOTTOM": {"name": "Brauchwasser unten", "id": "01215284cd72"},
                      "BU_TOP": {"name": "Pufferspeicher oben", "id": "0121523cf5e2"},
                      "SO_TOP": {"name": "Solarmodul oben", "id": "01215221f297"},
                      "CI_PIPE": {"name": "Zirkuleitung", "id": "0121528503c8"},
                      "OUT": {"name": "Außentemperatur", "id": "012152368b2b"},
                      }

SWITCHES = {
    "loading_pump": {"id": "1", "name": "Ladepumpe", "gpiopin": 17, "pin_nr": "pin11"},
    "heating_cooling": {"id": "2", "name": "Heizen/kuehlen", "gpiopin": 27, "pin_nr": "pin13"},
    "circulation_pump": {"id": "3", "name": "Zirkupumpe", "gpiopin": 22, "pin_nr": "pin15"},
    "solar_pump": {"id": "4", "name": "Solarpumpe", "gpiopin": 23, "pin_nr": "pin16"},
    "garden_water": {"id": "5", "name": "Bewaesserung", "gpiopin": 24, "pin_nr": "pin18"},
    "empty_pipes": {"id": "6", "name": "Leitungen ablassen", "gpiopin": 25, "pin_nr": "pin22"},
    "alarm": {"id": "7", "name": "Summer Alarm", "gpiopin": 5, "pin_nr": "pin29"},
    "electrical_heating_service_water": {"id": "8", "name": "Brauchwasser elektrisch heizen", "gpiopin": 6, "pin_nr": "pin31"}
}

PUMPS = ["loading_pump", "circulation_pump", "solar_pump"]

SW_HYSTERESE = {"lower": 42.5, "upper": 43.5}
SW_BU_HYSTERESE = {"lower": 6.5, "upper": 7.5}
SO_DELTA_HYSTERESE = {"lower": 6.0, "upper": 7.0}
