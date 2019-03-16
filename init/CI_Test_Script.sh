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
TELEGRAM_TOKEN=${BOT_API_KEY}
export BOT_API_KEY PARSE_BRANCH PARSE_ORIGIN COMMIT_POINT TELEGRAM_TOKEN

kickstart_pub

req_install() {
    pip install -r requirements.txt
}

get_session() {
    curl -sLo userbot.session "$PULL_LINK"
}

test_run() {
    python3 -m userbot test
}

trap '{
    STATUS=${?}
    tg_senderror
    finerr
}' ERR

tg_senderror() {
    tg_sendinfo "Build Throwing Error(s)" \
        "@baalajimaestro @raphielscape naaaaa"
    tg_channelcast "Build Throwing Error(s)"

    [ -n "${STATUS}" ] &&
    exit "${STATUS}" ||
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
    fin
}

get_session
execute