#!/bin/bash
# Copyright (C) 2020 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# CI Runner Script for Paperplane CI

# We need this directive
# shellcheck disable=1090

export SEMAPHORE_PROJECT_DIR=`pwd`
. "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"/telegram
TELEGRAM_TOKEN=${BOT_API_KEY}
export BOT_API_KEY TELEGRAM_TOKEN
tg_sendinfo "<code>I am gonna merge staging into master</code>"
cd
git clone https://github.com/RaphielGang/Telegram-Paperplane.git
cd Telegram-Paperplane
git remote set-url origin https://${GH_USERNAME}:${GH_PERSONAL_TOKEN}@github.com/RaphielGang/Telegram-Paperplane.git
git fetch
git checkout staging
git pull origin staging
git push --force origin staging:master
tg_sendinfo "<code>I have merged all commits from staging into master</code>"
