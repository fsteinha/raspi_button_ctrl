#!/bin/bash
# This a script for installing the raspi-button-ctrl as servic on a rasperrpi

# Check sudo rights
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# check for raspberry pi
SYSTEM_STR=${uname --all}
if echo "$SYSTEM_STR" | grep -q "raspberrypi"; then
    :
else
    echo "System string includes NOT raspberrypi"
    exit
fi

# copy sources to opt 
cp -r ../raspi_button_ctrl /opt/

# copy the service file 
cp raspi_button_ctrl.service /etc/systemd/system

# please reboot
echo "Please reboot the system"



