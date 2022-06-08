#!/usr/bin/env bash

export bolt_driving_blue_model=$(bolt_cache read blue_driver.release)

if [ ! -z "$bolt_driving_blue_model" ] ; then
    bolt_log "driving_blue: blue_driver[$bolt_driving_blue_model]"
    bolt_download asset $bolt_driving_blue_model

    bolt_relation set $bolt_driving_blue_model $bolt_asset_name ran-prediction-on
fi

bolt_blue drive