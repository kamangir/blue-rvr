#!/usr/bin/env python3
# This file is automatically generated!
# Source File:        0x13-power.json
# Device ID:          0x13
# Device Name:        power
# Timestamp:          05/28/2020 @ 20:39:42.003486 (UTC)

from enum import IntEnum


__all__ = ['BatteryVoltageStatesEnum',
           'BatteryVoltageReadingTypesEnum',
           'AmplifierIdsEnum']


class CommandsEnum(IntEnum): 
    sleep = 0x01
    wake = 0x0D
    get_battery_percentage = 0x10
    get_battery_voltage_state = 0x17
    will_sleep_notify = 0x19
    did_sleep_notify = 0x1A
    enable_battery_voltage_state_change_notify = 0x1B
    battery_voltage_state_change_notify = 0x1C
    get_battery_voltage_in_volts = 0x25
    get_battery_voltage_state_thresholds = 0x26
    get_current_sense_amplifier_current = 0x27


class BatteryVoltageStatesEnum(IntEnum):
    unknown = 0
    ok = 1
    low = 2
    critical = 3


class BatteryVoltageReadingTypesEnum(IntEnum):
    calibrated_and_filtered = 0
    calibrated_and_unfiltered = 1
    uncalibrated_and_unfiltered = 2


class AmplifierIdsEnum(IntEnum):
    left_motor = 0
    right_motor = 1
