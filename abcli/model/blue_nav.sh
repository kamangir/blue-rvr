#!/usr/bin/env bash

function abcli_blue_nav_annotated_assets() {
    abcli_nav_annotated_assets blue cube
}

function abcli_blue_nav_assets() {
    abcli_nav_assets blue cube
}

function abcli_blue_nav_ingest() {
    abcli_ingest_frames $(abcli_blue_nav_annotated_assets) sem_seg $@
}

function abcli_blue_nav_predict() {
    abcli_nav_predict $@
}

function abcli_blue_nav_train() {
    abcli_nav_train $@
}