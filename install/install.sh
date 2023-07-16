#!/bin/bash
# This a script for installing the raspi-button-ctrl as servic on a rasperrpi

# Check sudo rights
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# check for raspberry pi
SYSTEM_STR=$(uname --all)
if echo "$SYSTEM_STR" | grep -q "raspberrypi"; then
    :
else
    echo "System string includes NOT raspberrypi"
    exit
fi

# Stop running service
SERVICE_STATE=$(systemctl is-active raspi-button-ctrl.service)
if [ $SERVICE_STATE = "active" ]; then
  systemctl stop raspi-button-ctrl.service 
fi

# copy sources to opt 
cp -r ../raspi-button-ctrl /opt/

# copy the service file 
cp raspi-button-ctrl.service /etc/systemd/system
chmod 755 /etc/systemd/system/raspi-button-ctrl.service

# start service
systemctl start raspi-button-ctrl.service 

SERVICE_STATE=$(systemctl is-active raspi-button-ctrl.service)
if [ $SERVICE_STATE = "inactive" ]; then
  echo "Start service failed"
fi




