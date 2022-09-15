import sys
import time
from flask import request

from flask import Flask
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO

from demax_backend.configs import SWITCHES
from demax_backend.services.actors.relais import Switch

app = Flask(__name__)


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/switches')
def get_switches_states():
    res = {}
    for id, values in SWITCHES.items():
        s = Switch(values["gpiopin"], values["name"])
        res[id] = str(s.get_state())

    return res


@app.route('/switch', methods=['POST'])
def set_switch_state():
    switch_id = request.args.get('switch_id', None)
    target_state = request.args.get('target_state', None)
    config = SWITCHES[switch_id]
    s = Switch(config["gpiopin"], config["name"])
    if target_state == "0":
        s.set_low()
    if target_state == "1":
        s.set_high()
    return {}


app.run()