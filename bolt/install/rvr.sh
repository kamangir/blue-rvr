#! /usr/bin/env bash

if [ "$bolt_is_rpi" == true ] ; then
    bolt_rvr_revision="102"

    if [ -f "${bolt_path_git}/bolt_install_rvr_${bolt_rvr_revision}_complete" ] ; then
        bolt_log "verified rvr ${bolt_rvr_revision}."
    else
        bolt_log "installing rvr ${bolt_rvr_revision}..."

        # https://github.com/sphero-inc/sphero-sdk-raspberrypi-python/blob/master/first-time-setup.sh
        sudo apt-get update -y

        sudo apt-get install -y make \
            build-essential \
            llvm \
            libssl-dev \
            bzip2 \
            zlib1g-dev \
            libbz2-dev \
            libreadline6 \
            libreadline-dev \
            libsqlite3-dev \
            libncurses5-dev \
            libncursesw5-dev \
            xz-utils \
            tk-dev \
            libffi-dev \
            liblzma-dev

        # python -m pip install pipenv

        # printf "PATH=$HOME/.local/bin:$PATH\n" >> ~/.profile

        # https://github.com/sphero-inc/sphero-sdk-raspberrypi-python/blob/master/Pipfile
        sudo python3 -m pip install aiohttp
        sudo python3 -m pip install requests
        sudo python3 -m pip install websocket-client
        sudo python3 -m pip install pytest-asyncio
        sudo python3 -m pip install pytest
        sudo python3 -m pip install twine
        sudo python3 -m pip install pyserial
        sudo python3 -m pip install pyserial-asyncio

        touch ${bolt_path_git}/bolt_install_rvr_${bolt_rvr_revision}_complete
    fi

fi