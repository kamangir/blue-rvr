#! /usr/bin/env bash

if [ "$abcli_is_rpi" == true ] ; then
    abcli_rvr_revision="102"

    if [ -f "${abcli_path_git}/abcli_install_rvr_${abcli_rvr_revision}_complete" ] ; then
        abcli_log "verified rvr ${abcli_rvr_revision}."
    else
        abcli_log "installing rvr ${abcli_rvr_revision}..."

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

        touch ${abcli_path_git}/abcli_install_rvr_${abcli_rvr_revision}_complete
    fi

fi