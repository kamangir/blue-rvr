#!/usr/bin/env python3
# This file is automatically generated!
# Source File:        0x1A-user_io.json
# Device ID:          0x1A
# Device Name:        io
# Timestamp:          03/31/2020 @ 20:26:27.200112 (UTC)

from enum import IntEnum


__all__ = ['SpecdrumsColorPaletteIndiciesEnum']


class CommandsEnum(IntEnum): 
    set_all_leds = 0x1A
    get_active_color_palette = 0x44
    set_active_color_palette = 0x45
    get_color_identification_report = 0x46
    load_color_palette = 0x47
    save_color_palette = 0x48
    release_led_requests = 0x4E


class SpecdrumsColorPaletteIndiciesEnum(IntEnum):
    default = 0
    midi = 1
