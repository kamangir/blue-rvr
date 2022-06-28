from sphero_sdk import SpheroRvrAsync
from sphero_sdk import SerialAsyncDal
from .helper_keyboard_input import KeyboardHelper
import cv2
import numpy as np
import os
import sys

import abcli.assets as assets
import abcli.annotation as annotation
import abcli.file as file
from abcli.hardware import instance as hardware
import abcli.host as host
from abcli.looper import Looper
from training_framework.model.image_classifier import image_classifier
import abcli.string as string
from abcli.timer import Timer

import abcli.logging
import logging


import asyncio
from rtcbot import PiCamera

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


abcli_asset_name = os.getenv("abcli_asset_name")

pulse = Timer(host.arguments.get("blue.pulse", 3), "blue.pulse")


# initialize global variables
key_helper = KeyboardHelper()
current_key_code = -1
driving_keys = [119, 97, 115, 100, 32]
speed = 0
heading = 0
going_backward = False

turn_left = 100  # D
turn_right = 97  # A
go_forward = 119  # W
go_backward = 115  # S
exit_command = 111  # O
update_command = 117  # u
help_command = 104  # h
run_model_command = 109  # m
run_model_always_command = 110  # n

loop = asyncio.get_event_loop()

looper = Looper()

abcli_asset_folder = os.getenv("abcli_asset_folder")

camera_enabled = host.arguments.get("blue.camera.enabled", True)
model_asset = os.getenv("abcli_driving_blue_model")

if model_asset:
    logger.info("blue: model={}".format(model_asset))

    classifier = image_classifier()
    if not classifier.load(assets.path_of(model_asset)):
        model_asset = ""

if camera_enabled:
    camera = PiCamera()

    @camera.subscribe
    def onFrame(frame):
        global frame_number
        global save_frame
        global run_model
        global prediction
        global pulse

        if not (pulse.tick() or run_model == True or save_frame):
            return

        if not save_frame:
            if run_model:
                success, prediction = classifier.predict_frame(frame)

                run_model = False if run_model == True else run_model

                if success:
                    save_frame = annotation.store(
                        abcli_asset_name,
                        frame_number,
                        "live_blue_driver",
                        prediction,
                    )
            else:
                save_frame = annotation.store(
                    abcli_asset_name,
                    frame_number,
                    "current_key_code",
                    0,
                )

        hardware.output(hardware.data_pin, prediction != -1)
        hardware.output(hardware.outgoing_pin, save_frame)

        if save_frame:
            file.save_image(
                os.path.join(
                    abcli_asset_folder, "Data/{}/camera.jpg".format(frame_number)
                ),
                frame,
            )

            logger.info(
                "frame #{}: {}".format(
                    frame_number, string.pretty_size_of_matrix(frame)
                )
            )

            frame_number += 1
        save_frame = False


rvr = SpheroRvrAsync(dal=SerialAsyncDal(loop))


def keycode_callback(keycode):
    global current_key_code
    current_key_code = keycode
    print("Key code updated: ", str(current_key_code))


speed_level = 32
max_speed_level = 96

frame_number = -1
save_frame = False
run_model = False  # False,True,"always" <- always
prediction = -1


async def main():
    """
    Runs the main control loop for this demo.  Uses the KeyboardHelper class to read a keypress from the terminal.

    W - Go forward.  Press multiple times to increase speed.
    A - Decrease heading by -10 degrees with each key press.
    S - Go reverse. Press multiple times to increase speed.
    D - Increase heading by +10 degrees with each key press.
    Spacebar - Reset speed and going_backward to 0. RVR will coast to a stop

    """
    global current_key_code
    global speed
    global heading
    global going_backward
    global frame_number
    global save_frame
    global run_model
    global prediction
    global pulse

    def get_status():
        return "blue.drive: {} {} @ {} deg".format(
            speed, "backward" if going_backward else "forward", heading
        )

    await rvr.wake()

    await rvr.reset_yaw()

    logger.info("blue.main() started...")

    previous_status = ""
    while True:
        hardware.pulse(hardware.looper_pin)

        if looper.check_switch() == False:
            break

        reset_pulse = True

        if current_key_code != -1 and frame_number != -1:
            save_frame = annotation.store(
                abcli_asset_name,
                frame_number,
                "current_key_code",
                current_key_code,
            )

        if current_key_code == go_forward:
            if going_backward:
                speed -= speed_level
                logger.info("blue.drive: speed down.")

                if speed <= 0:
                    going_backward = False
            else:
                logger.info("blue.drive: speed up.")
                speed += speed_level
        elif current_key_code == turn_right or prediction == 1:
            heading -= 10
            logger.info("blue.drive: turning right")
        elif current_key_code == go_backward:
            if not going_backward:
                speed -= speed_level
                logger.info("blue.drive: speed down.")

                if speed <= 0:
                    going_backward = True
            else:
                speed += speed_level
                logger.info("blue.drive: speed up.")
        elif current_key_code == turn_left or prediction == 0:
            heading += 10
            logger.info("blue.drive: turning left.")
        elif current_key_code == 32:  # SPACE
            logger.info("blue.drive: stop.")
            speed = 0
            going_backward = False
        elif current_key_code == 112:  # P
            host.return_to_bash("shutdown")
            break
        elif current_key_code == exit_command:
            host.return_to_bash("exit")
            break
        elif current_key_code == update_command:
            host.return_to_bash("update")
            break
        elif current_key_code == help_command:
            show_help()
        elif current_key_code == run_model_command:
            run_model = True
        elif current_key_code == run_model_always_command:
            run_model = False if run_model == "always" else "always"
        else:
            reset_pulse = False

        if reset_pulse:
            pulse.reset()

        prediction = -1

        speed = max(0, min(speed, max_speed_level))

        if heading > 359:
            heading = heading - 359
        elif heading < 0:
            heading = 359 + heading

        status = get_status()
        if status != previous_status:
            logger.info(status)
            previous_status = status

        current_key_code = -1

        await rvr.drive_with_heading(speed, heading, going_backward)

        # avoid flooding the serial port.
        await asyncio.sleep(0.1)


def run_loop():
    global loop
    global key_helper
    key_helper.set_callback(keycode_callback)
    loop.run_until_complete(asyncio.gather(main()))


def show_help():
    print("o - exit.")
    print("P - shutdown.")
    print("m - run the model.")
    print("n - run the model continuously.")
    print("h - show help.")
    print("u - update.")
    print("w - fwd, faster.")
    print("a - turn 10 deg right.")
    print("s - reverse, faster.")
    print("d - turn 10 deg left.")
    print("Spacebar - Stop.")
