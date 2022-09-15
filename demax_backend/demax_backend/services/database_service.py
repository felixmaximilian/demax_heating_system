from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
from demax_backend.services.actors.relais import Switch
from demax_backend.services.sensors.temperature_service import DS18B20

token = "AEpR48seLt28NC2-bNfWabPv5ierk-wcR8vWWnJNTFnr_f04LI7VZ6OP7tnLnMGfn3auk9WzElVPb96P40c7vQ=="
org = "demax"
bucket = "temperature"

influx_url = "http://localhost:8086"  # TODO: once using docker, use http://influxdb:8086

# TODO: Use intermediate Temperature object and remove this files dependency to DS18B20 (migrate to temperature_service)
def update_temperatures(sensor_mapping):
    for sensor_name, sensor_config in sensor_mapping.items():
        sensor = DS18B20.get_sensor(sensor_config["id"])
        temperature = sensor.get_temperature()
        description = sensor_config["name"]
        write_temperature_sensor_data(sensor.get_id(), description, temperature)



def write_temperature_sensor_data(id, description, temperature):
    with InfluxDBClient(url=influx_url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        point = Point("temperature") \
            .tag("host", "host1") \
            .tag("id", id) \
            .tag("description", description) \
            .field("temperature", temperature) \
            .time(datetime.utcnow(), WritePrecision.NS)

        write_api.write(bucket, org, point)


def update_switches_data(switches):
    for switch_id, sensor_config in switches.items():
        switch = Switch(sensor_config["gpiopin"], sensor_config["name"])
        value = switch.get_state()
        description = sensor_config["name"]
        write_switch_data(switch_id, description, value)

def write_switch_data(id, description, value):
    with InfluxDBClient(url=influx_url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        point = Point("switch") \
            .tag("host", "host1") \
            .tag("id", id) \
            .tag("description", description) \
            .field("state", value) \
            .time(datetime.utcnow(), WritePrecision.NS)

        write_api.write(bucket, org, point)

def write_data():
    with InfluxDBClient(url=influx_url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)

        point = Point("mem") \
            .tag("host", "host1") \
            .field("sensor1", 42.1) \
            .time(datetime.utcnow(), WritePrecision.NS)

        write_api.write(bucket, org, point)


def read_data():
    with InfluxDBClient(url=influx_url, token=token, org=org) as client:

        query = 'from(bucket: "temperature") |> range(start: -1h)'
        tables = client.query_api().query(query, org=org)
        for table in tables:
            for record in table.records:
                print(record)
