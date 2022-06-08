#!/usr/bin/env bash

function bolt_blue_nav_annotated_assets() {
    bolt_nav_annotated_assets blue cube
}

function bolt_blue_nav_assets() {
    bolt_nav_assets blue cube
}

function bolt_blue_nav_ingest() {
    bolt_ingest_frames $(bolt_blue_nav_annotated_assets) sem_seg $@
}

function bolt_blue_nav_predict() {
    bolt_nav_predict $@
}

function bolt_blue_nav_train() {
    bolt_nav_train $@
}