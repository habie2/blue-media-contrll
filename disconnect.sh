#!/bin/bash

DEVICE_MAC="8C:86:1E:5F:FA:8B"

echo -e "disconnect $DEVICE_MAC\nquit" | bluetoothctl
