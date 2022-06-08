#!/usr/bin/env bash

function bolt_blue() {
    local task=$(bolt_unpack_keyword $1 help)

    if [ "$task" == "help" ] ; then
        bolt_help_line "blue drive" \
            "drive blue."
        bolt_help_line "blue publish" \
            "publish blue-rvr."
        bolt_help_line "blue validate" \
            "validate blue."
        return
    fi

    if [ "$task" == "drive" ] ; then
        bolt_log "blue started driving..."

        bolt_select

        bolt_host tag driving_blue .

        python3 -m blue

        bolt_upload open
        bolt_tag set . $(bolt_host get tags),$bolt_host_name,$(bolt_string_today),$bolt_fullname,${bolt_wifi_ssid},annotated

        bolt_log "blue stopped driving..."
        return
    fi

    if [ "$task" == "publish" ] ; then
        bolt_git clone blue-rvr pull

        mkdir -p $bolt_path_git/blue-rvr/blue/

        cp -Rv $bolt_path_git/blue/bolt/* $bolt_path_git/blue-rvr/bolt/
        cp -Rv $bolt_path_git/blue/blue/* $bolt_path_git/blue-rvr/blue/

        bolt_git cd blue-rvr
        git status
        return
    fi

    if [ "$task" == "validate" ] ; then
        pushd $bolt_path_git/blue/projects/keyboard_control > /dev/null
        python3 drive_with_wasd_keys.py
        popd  > /dev/null
        return
    fi

    bolt_log_error "unknown task: blue '$task'."
}