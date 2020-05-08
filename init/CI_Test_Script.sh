#!/bin/bash
# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# CI Runner Script for Paperplane CI

# We need this directive
# shellcheck disable=1090

. "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"/telegram

PARSE_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
PARSE_ORIGIN="$(git config --get remote.origin.url)"
COMMIT_POINT="$(git log --pretty=format:'%h : %s' -1)"
COMMIT_HASH="$(git rev-parse --verify HEAD)"
REVIEWERS="@zakaryan2004"
TELEGRAM_TOKEN=${BOT_API_KEY}
export BOT_API_KEY PARSE_BRANCH PARSE_ORIGIN COMMIT_POINT TELEGRAM_TOKEN
kickstart_pub

req_install() {
    pip3 install --upgrade setuptools pip
    pip3 install -r requirements.txt
    pip3 install yapf
}

test_run() {
    python3 -m userbot
    STATUS=${?}
    export STATUS
}

tg_senderror() {
    if [ ! -z "$PULL_REQUEST_NUMBER" ]; then
        tg_sendinfo "<code>This PR is having build issues and won't be merged until it's fixed<code>"
        exit 1
    fi
    tg_sendinfo "<code>Build Throwing Error(s)!</code>" \
        "${REVIEWERS} please look in!" \
        "Logs: https://semaphoreci.com/zakaryan2004/telegram-paperplane"

    [ -n "${STATUS}" ] &&
    exit "${STATUS}" ||
    exit 1
}

lint() {
  if [ ! -z "$PULL_REQUEST_NUMBER" ]; then
    exit 0
  fi

  RESULT=`yapf -d -r -p userbot`

  if [ ! -z "$RESULT" ]; then
    tg_sendinfo "<code>Code has lint issues, but hasn't been linted.</code>"
  else
    tg_sendinfo "<code>Code doesn't have any lint issues.</code>"
  fi
}
tg_yay() {
  if [ ! -z "$PULL_REQUEST_NUMBER" ]; then

      tg_sendinfo "<code>Compilation success! Checking for lint issues.</code>"
      if ! yapf -d -r -p userbot; then
        tg_sendinfo "<code>PR has lint problems.</code>"
        exit 1
      else
        tg_sendinfo "<code>PR doesn't have any lint problems.</code>"
        exit 0
      fi
   fi
    tg_sendinfo "<code>Compilation success!</code>"
    lint
}

# Fin Prober
fin() {
    echo "Job completed successfully ($((DIFF / 60)) minute(s) and $((DIFF % 60)) seconds)."
    tg_yay
}

finerr() {
    echo "Job failed ($((DIFF / 60)) minute(s) and $((DIFF % 60)) seconds)"
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

execute
