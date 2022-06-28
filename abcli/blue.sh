#!/usr/bin/env bash

function blue() {
    abcli_blue $@
}

function abcli_blue() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ "$task" == "help" ] ; then
        abcli_help_line "blue drive" \
            "drive blue."
        abcli_help_line "blue publish" \
            "publish blue-rvr."
        abcli_help_line "blue validate" \
            "validate blue."
        return
    fi

    if [ "$task" == "drive" ] ; then
        abcli_log "blue started driving..."

        abcli_select

        abcli_host tag driving_blue .

        python3 -m blue

        abcli_upload open
        abcli_tag set . $(abcli_host get tags),$abcli_host_name,$(abcli_string_today),$abcli_fullname,${abcli_wifi_ssid},annotated

        abcli_log "blue stopped driving..."
        return
    fi

    if [ "$task" == "publish" ] ; then
        abcli_git clone blue-rvr pull

        mkdir -p $abcli_path_git/blue-rvr/blue/
        mkdir -p $abcli_path_git/blue-rvr/abcli/

        cp -Rv $abcli_path_git/blue/abcli/* $abcli_path_git/blue-rvr/abcli/
        cp -Rv $abcli_path_git/blue/blue/* $abcli_path_git/blue-rvr/blue/

        abcli_git cd blue-rvr
        git status
        return
    fi

    if [ "$task" == "validate" ] ; then
        pushd $abcli_path_git/blue/projects/keyboard_control > /dev/null
        python3 drive_with_wasd_keys.py
        popd  > /dev/null
        return
    fi

    abcli_log_error "-blue: $task: command not found."
}