#!/bin/bash
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
# CI Runner Script for baalajimaestro's userbot

# We need this directive
# shellcheck disable=1090

. "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"/telegram

PARSE_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
PARSE_ORIGIN="$(git config --get remote.origin.url)"
COMMIT_POINT="$(git log --pretty=format:'%h : %s' -1)"
COMMIT_HASH="$(git rev-parse --verify HEAD)"
TELEGRAM_TOKEN=${BOT_API_KEY}
export BOT_API_KEY PARSE_BRANCH PARSE_ORIGIN COMMIT_POINT TELEGRAM_TOKEN

kickstart_pub

req_install() {
    pip3 install -r requirements.txt
}

get_session() {
    curl -sLo userbot.session "$PULL_LINK"
}

test_run() {
    python3 -m userbot test
    STATUS=${?}
    export STATUS
}

# Nuke Trap, coz it not working

tg_senderror() {
    tg_sendinfo "<code>Build Throwing Error(s)</code>" \
        "@baalajimaestro @raphielscape @MrYacha please look in!" \
        "Logs: https://semaphoreci.com/baalajimaestro/telegram-userbot"

    [ -n "${STATUS}" ] &&
    exit "${STATUS}" ||
    exit 1
}

tg_yay() {
    tg_sendinfo "<code>Compilation Success!</code>"
}

# Fin Prober
fin() {
    echo "Yay! My works took $((DIFF / 60)) minute(s) and $((DIFF % 60)) seconds.~"
    tg_yay
}

finerr() {
    echo "My works took $((DIFF / 60)) minute(s) and $((DIFF % 60)) seconds but it's error..."
    tg_senderror

    [ -n "${STATUS}" ] &&
    exit "${STATUS}" ||
    exit 1
}

execute() {
    BUILD_START=$(date +"%s")
        req_install
        test_run
    BUILD_END=$(date +"%s")
    DIFF=$((BUILD_END - BUILD_START))
    if [ $STATUS -eq 0 ];
    then
    fin
    else
    finerr
    fi
}

get_session
execute