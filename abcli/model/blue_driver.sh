#!/usr/bin/env bash

function abcli_blue_driver_annotated_assets() {
    abcli_tag search annotated,driving_blue,${abcli_tag_ignore_list} --host 0 --raw 1
}

function abcli_blue_driver_assets() {
    abcli_tag search driving_blue,${abcli_tag_ignore_list} --host 0 --raw 1
}

function abcli_blue_driver_ingest() {
    abcli_ingest_frames $(abcli_blue_driver_annotated_assets) current_key_code $@
}

function abcli_blue_driver_predict() {
    abcli_blue_driver_preprocess predict $1
    abcli_image_classifier_predict $@
}

function abcli_blue_driver_preprocess() {
    local purpose=$1
    local data_asset=$2
    abcli_log "blue_driver.preprocess($purpose:$data_asset)"

    python3 -m blue.model.blue_driver \
        preprocess \
        --data_asset $data_asset \
        --purpose $purpose \
        ${@:3}
}

function abcli_blue_driver_train() {
    abcli_blue_driver_preprocess train $1
    abcli_image_classifier_train $@
}