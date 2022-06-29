import argparse
import cv2
from functools import reduce
import numpy as np
import os.path


import abcli.annotation as annotation
import abcli.assets as assets
import abcli.cache as cache
import abcli.file as file
from abcli.options import Options
import abcli.string as string

import abcli.logging
import logging

logger = logging.getLogger(__name__)

name = "blue_driver"

class_names = "turn_left,turn_right,no_action".split(",")
current_key_code_values = "100,97".split(",")
# turn_left = 100  # D
# turn_right = 97  # A
# ref: abcli/algo/blue/__main__.py

window_size = 128


def preprocess(data_asset, options=""):
    options = (
        Options(options).default("purpose", "predict").default("test_size", 1.0 / 6)
    )

    logger.info("blue_driver.preprocess({}:{})".format(options["purpose"], data_asset))

    data_asset_path = assets.path_of(data_asset)

    if options["purpose"] == "train":
        if not file.save_json(
            os.path.join(data_asset_path, "class_names"), class_names
        ):
            return False

        if not cache.write("{}.window_size".format(data_asset), str(window_size)):
            return False

    if options["purpose"] in "eval,train".split(","):
        success, frames = annotation.status_of_asset(data_asset, "current_key_code")
        if not success:
            return success

        frames = {frame: frames[frame][0][1] for frame in frames}
        logger.info(
            string.pretty_list(
                [
                    "#{}:#{}".format(frame, current_key_code)
                    for frame, current_key_code in frames.items()
                ],
                "items=frame(s)",
            )
        )

    if options["purpose"] == "predict":
        frames = {frame: "666" for frame in assets.list_of_frames(data_asset, "name")}
        print(data_asset)

    images = np.zeros((len(frames), window_size, window_size, 3), dtype=np.uint8)
    labels = np.zeros((len(frames),), dtype=np.uint8)
    index = 0
    for frame, current_key_code in frames.items():
        filename = os.path.join(data_asset_path, "Data", str(frame), "camera.jpg")
        success_, image = file.load_image(filename)
        if not success_:
            continue

        try:
            images[index] = cv2.resize(image, (window_size, window_size))
        except:
            continue

        labels[index] = (
            current_key_code_values.index(current_key_code)
            if current_key_code in current_key_code_values
            else len(current_key_code_values)
        )
        logger.info("#{}: {}".format(labels[index], filename))

        index += 1

    images = images[:index]
    labels = labels[:index]
    if index < len(frames):
        logger.error(f"-{name}: preprocess: {len(frames) - index} bad frame(s).")
    logger.info(
        string.pretty_list(
            labels, {"binned": True, "class_names": class_names, "items": "frame(s)"}
        )
    )

    if options["purpose"] == "predict":
        return file.save_tensor(
            os.path.join(data_asset_path, "test_images.pyndarray"), images
        )

    if options["purpose"] == "eval":
        return file.save_tensor(
            os.path.join(data_asset_path, "test_labels.pyndarray"), labels
        )

    if options["purpose"] == "train":
        from sklearn.model_selection import train_test_split

        train_images, test_images, train_labels, test_labels = train_test_split(
            images, labels, test_size=options["test_size"]
        )

        return reduce(
            lambda x, y: x and y,
            [
                file.save_tensor(
                    os.path.join(data_asset_path, "{}.pyndarray".format(name)), tensor
                )
                for tensor, name in zip(
                    [train_images, test_images, train_labels, test_labels],
                    "train_images,test_images,train_labels,test_labels".split(","),
                )
            ],
            True,
        )

    logger.error(
        f"-blue: blue_driver: preprocess: {options['purpose']} purpose not found."
    )
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "task",
        type=str,
        default="",
        help="preprocess",
    )
    parser.add_argument(
        "--data_asset",
        type=str,
        default="",
        help="",
    )
    parser.add_argument(
        "--purpose",
        type=str,
        default="predict",
        help="eval/predict/train",
    )
    args = parser.parse_args()

    success = False
    if args.task == "preprocess":
        success = preprocess(
            args.data_asset,
            {
                "purpose": args.purpose,
            },
        )
    else:
        logger.error(f"-{name}: {args.task}: command not found.")

    if not success:
        logger.error(f"-{name}: {args.task}: failed.")
