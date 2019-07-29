import sys
sys.path.append('/home/pi/raspberry-pi-python')

import time
from sphero_sdk import ObserverSpheroRvr

rvr = ObserverSpheroRvr()

def on_battery_percentage_info(**kwargs):
    print("Current battery percentage: ", kwargs["percentage"], "%")

def on_battery_volt_state_info(**kwargs):
    state_info = {0: "unknown", 1: "OK", 2: "low", 3: "critical"}
    print("Voltage states: ", state_info)
    print("Current voltage state: ", kwargs["state"])




def main():
    """ This program demonstrates how to retrieve the battery state of RVR and print it to the console.

    """
    rvr.wake()

    rvr.get_battery_percentage(on_battery_percentage_info)

    rvr.get_battery_voltage_state(on_battery_volt_state_info)

    # Sleep for one second such that RVR has time to send data back
    time.sleep(1)

    rvr.close()



main()