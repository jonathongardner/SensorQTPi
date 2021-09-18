## What is SensorQTPi

SensorQTPi is an implementation that provides methods to communicate with a Raspberry Pi sensor via the MQTT protocol.
Although it is designed to work out of the box with a Home Assistant cover component it can also be used as the basis for any Raspberry Pi sensor (right now only DHT11 and DHT22 sensors are implemented).

## Motivation

Home Assistant has integration for raspberry pi sensors but only if the instance of Home Assistant is running on the raspberry pi. If your raspberry pi is only used for sensors then you need to use an MQTT component to interface with the pi.

## Software

### Prereqs
* Raspberry pi 3 running rasbian jessie
* Python 2.7.x
* pip (python 2 pip)

### Installation
1. `git clone https://github.com/jonathongardner/SensorQTPi.git`
2. `pip install -r requirements.txt`
3. edit the configuration.yaml to set up mqtt (See below)
4. `python main.py`
5. To start the server on boot run `sudo bash autostart_systemd.sh`

## MQTT setup
MQTT setup guide resources:

HomeAssistant MQTT Setup: https://home-assistant.io/components/mqtt/

Bruh Automation: https://www.youtube.com/watch?v=AsDHEDbyLfg

## Home Assistant component setup
Either follow the cover setup or enable mqtt discovery  
HomeAssistant MQTT Sensor: https://home-assistant.io/components/sensor.mqtt/  
HomeAssistant MQTT Discovery: https://home-assistant.io/docs/mqtt/discovery/

Screenshot:

![Home assistant ui][1]

## Sample Configuration

config.yaml:
```
mqtt:
    host: m10.cloudmqtt.com
    port: *
    user: *
    password: *
sensors:
    -
        id: 'outside'
        pin: 23
        interval: 30 # minutes
        state_topic: "home-assistant/outside"
    -
        id: 'garage'
        pin: 24
        interval: 20 # minutes
        state_topic: "home-assistant/garage"
```

### Optional configuration
There are three optional configuration parameters.  
Two of the option parameters are for mqtt. One is to enable discovery by HomeAssistant. The second one changes the discovery prefix for HomeAssitant.
```
mqtt:
    host: m10.cloudmqtt.com
    port: *
    user: *
    password: *
    discovery: true
    discovery_prefix: 'homeassistant'
```

The discovery parameter defaults to false and should be set to true to enable discovery by HomeAssistant. If set to true, the sensor state_topic parameters are not necessary and are ignored.  
The discovery_prefix parameter defaults to 'homeassistant' and shouldn't be changed unless changed in HomeAssistant

The other option parameter is for the sensor. One to give the sensor a name for discovery.
```
sensors:
    -
        id: 'outside'
        name: 'Outside'
        state: 17
        interval: 5 # minutes
        state_topic: "home-assistant/cover/left"
```

The name parameter defaults to the unsanitized id parameter  

## Contributors

This code was forked from [GarageQTPi](https://github.com/Jerrkawz/GarageQTPi.git).
