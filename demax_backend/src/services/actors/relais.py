import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)  # GPIO Nummern statt Board Nummern

class Switch:
    def __init__(self, gpio_id, name):
        self.gpio_id = gpio_id
        self.name = name

    def get_state(self):
        GPIO.setup(self.gpio_id, GPIO.IN)
        return GPIO.input(self.gpio_id)

    def set_high(self):
        GPIO.setup(self.gpio_id, GPIO.OUT)
        logging.info(f'Schalte {self.name} ein...')
        GPIO.output(self.gpio_id, GPIO.HIGH)

    def set_low(self):
        GPIO.setup(self.gpio_id, GPIO.OUT)
        logging.info(f'Schalte {self.name} aus...')
        GPIO.output(self.gpio_id, GPIO.LOW)


class SwitchHolder:
    def __init__(self, switches_dict):
        self.switches = {
            key: Switch(values["gpiopin"], values["name"])
            for key, values in switches_dict.items()
        }

    def get(self, key):
        return self.switches[key]
