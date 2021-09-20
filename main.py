import os
import binascii
import yaml
import paho.mqtt.client as mqtt
import re
import json

from lib.sensor import Sensor

print("Welcome to SensorPi!")

# Update the mqtt state topic
def update_state(value, topic):
    print("Temperature check triggered: %s -> %s" % (topic, value))

    client.publish(topic, value, retain=True)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code: %s" % mqtt.connack_string(rc))

def sanitize_id(id):
    return re.sub('\W+', '', re.sub('\s', ' ', id))

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.yaml'), 'r') as ymlfile:
    CONFIG = yaml.load(ymlfile)

### SETUP MQTT ###
user = CONFIG['mqtt']['user'] or ''
password = CONFIG['mqtt']['password']
host = CONFIG['mqtt']['host']
port = int(CONFIG['mqtt']['port'])
discovery = bool(CONFIG['mqtt'].get('discovery'))
discovery_prefix = CONFIG['mqtt'].get('discovery_prefix', 'homeassistant')

client = mqtt.Client(client_id="MQTTGarageDoor_" + str(binascii.b2a_hex(os.urandom(6))), clean_session=True, userdata=None, protocol=4)

client.on_connect = on_connect

client.username_pw_set(user, password=password)
client.connect(host, port, 60)
### SETUP END ###

### MAIN LOOP ###
if __name__ == "__main__":
    # Create sensor objects and create callback functions
    for sensorCfg in CONFIG['sensors']:

        # If no name it set, then set to id
        if 'name' not in sensorCfg:
            sensorCfg['name'] = sensorCfg['id']

        # Sanitize id value for mqtt
        sensorCfg['id'] = sanitize_id(sensorCfg['id'])

        state_topic = sensorCfg['state_topic']

        sensor = Sensor(sensorCfg)

        def on_interval(value, topic=state_topic):
            update_state(json.dumps(value), topic)

        # You can add additional listeners here and they will all be executed when the sensor updates
        sensor.onInterval.addHandler(on_interval)

        # Publish initial sensor value
        sensor.start()

        # If discovery values publish configuration
        for dv in sensorCfg.get('discovery_values', []):
            dv['id'] = sanitize_id(dv['id'])

            # If no name it set, then set to id
            if 'name' not in dv:
                dv['name'] = dv['id']

            config_topic = '{dp}/sensor/{id_base}_{id}/config'.format(
                dp=discovery_prefix, id_base=sensorCfg['id'], id=dv['id']
            )
            config = {
                'name': '{name_base} {name}'.format(
                    name_base=sensorCfg['name'], name=dv['name']
                ),
                'state_topic': state_topic,
                'unit_of_measurement': dv['unit_of_measurement'],
                'value_template' : dv['template']
            }
            client.publish(config_topic, json.dumps(config), retain=True)

    # Main loop
    client.loop_forever()
