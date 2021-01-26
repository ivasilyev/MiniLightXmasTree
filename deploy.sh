#!/usr/bin/env bash

for FILE in __init__.py \
    animation_controller.py \
    animations.py \
    boot.py \
    color_utils.py \
    config.json \
    main.py \
    neo_rings.py \
    sensor_controller.py \
    utils.py
  do
    echo "Copy ${FILE}"
    ampy put "${FILE}"
  done
echo "Done, rebooting"
ampy reset
