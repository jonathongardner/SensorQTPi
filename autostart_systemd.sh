#!/bin/bash
cp garageqtpi@pi.service /etc/systemd/system/sensorqtpi@${SUDO_USER:-${USER}}.service
sed -i "s?/home/pi/SensorQTPi?`pwd`?" /etc/systemd/system/sensorqtpi@${SUDO_USER:-${USER}}.service
systemctl --system daemon-reload
systemctl enable sensorqtpi@${SUDO_USER:-${USER}}.service
