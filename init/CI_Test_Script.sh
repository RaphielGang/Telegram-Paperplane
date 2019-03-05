# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#

 
#! /bin/sh

#CI Runner Script for baalajimaestro's userbot

function colors {
	blue='\033[0;34m' cyan='\033[0;36m'
	yellow='\033[0;33m'
	red='\033[0;31m'
	nocol='\033[0m'
}

colors;
PARSE_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
PARSE_ORIGIN="$(git config --get remote.origin.url)"
COMMIT_POINT="$(git log --pretty=format:'%h : %s' -1)"
TELEGRAM_TOKEN=${BOT_API_KEY}
export BOT_API_KEY PARSE_BRANCH PARSE_ORIGIN COMMIT_POINT TELEGRAM_TOKEN
. "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"/telegram
kickstart_pub

function get_session {
    wget $PULL_LINK
}

function test_run {
	sudo apt install python3 python3-pip
    pip install -r requirements.txt
    python3 -m userbot test
    check_if_error
}

function check_if_error {
	if [ $? -eq 0 ]
    then
        fin
	else 
		finerr
	fi	
}

}
tg_senderror() {
    tg_sendinfo "Build Throwing Error(s)" \
    "@baalajimaestro naaaaa"
     tg_channelcast "Build Throwing Error(s)"
     exit 1
}

tg_yay() {
    tg_sendinfo "Python CI Test passed yay" \
    "Haha yes"
}

# Fin Prober
fin() {
    echo "Yay! My works took $((DIFF / 60)) minute(s) and $((DIFF % 60)) seconds.~"
    tg_sendinfo "Compilation took $((DIFF / 60)) minute(s) and $((DIFF % 60)) seconds"
    tg_channelcast "Compilation took $((DIFF / 60)) minute(s) and $((DIFF % 60)) seconds"
    tg_yay
}
finerr() {
    echo "My works took $((DIFF / 60)) minute(s) and $((DIFF % 60)) seconds but it's error..."
    tg_sendinfo "Build took $((DIFF / 60)) minute(s) and $((DIFF % 60)) seconds" \
                "but it is having error anyways xd"
    tg_senderror
    exit 1
}

get_session
test_run
