#!/usr/bin/env bash

export abcli_driving_blue_model=$(abcli_cache read blue_driver.release)

if [ ! -z "$abcli_driving_blue_model" ] ; then
    abcli_log "driving_blue: blue_driver[$abcli_driving_blue_model]"
    abcli_download asset $abcli_driving_blue_model

    abcli_relation set $abcli_driving_blue_model $abcli_asset_name ran-prediction-on
fi

abcli_blue drive