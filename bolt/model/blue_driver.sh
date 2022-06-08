#!/usr/bin/env bash

function bolt_blue_driver_annotated_assets() {
    bolt_tag search annotated,driving_blue,${bolt_tag_ignore_list} --host 0 --raw 1
}

function bolt_blue_driver_assets() {
    bolt_tag search driving_blue,${bolt_tag_ignore_list} --host 0 --raw 1
}

function bolt_blue_driver_ingest() {
    bolt_ingest_frames $(bolt_blue_driver_annotated_assets) current_key_code $@
}

function bolt_blue_driver_predict() {
    bolt_blue_driver_preprocess predict $1
    bolt_image_classifier_predict $@
}

function bolt_blue_driver_preprocess() {
    local purpose=$1
    local data_asset=$2
    bolt_log "blue_driver.preprocess($purpose:$data_asset)"

    python3 -m blue.model.blue_driver \
        preprocess \
        --data_asset $data_asset \
        --purpose $purpose \
        ${@:3}
}

function bolt_blue_driver_train() {
    bolt_blue_driver_preprocess train $1
    bolt_image_classifier_train $@
}