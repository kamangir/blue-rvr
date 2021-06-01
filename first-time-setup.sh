#!/bin/bash

# This script guides a user through setting up the Sphero RVR Python SDK.

# Install the SDK dependencies
pip3 install -r requirements.txt

# Provide an opportunity to correct the UART settings if needed.
./tools/pi-uart-check.sh