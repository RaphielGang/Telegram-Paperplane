#!/bin/bash
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# CI Runner Script for baalajimaestro's userbot

# We need this directive
# shellcheck disable=1090

export SEMAPHORE_PROJECT_DIR=`pwd`
. "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"/telegram
TELEGRAM_TOKEN=${BOT_API_KEY}
export BOT_API_KEY TELEGRAM_TOKEN
tg_sendinfo "<code>I am gonna merge staging into master</code>"
cd
git clone https://github.com/MyPaperPlane/Telegram-UserBot.git
cd Telegram-UserBot
git remote rm origin
git remote add origin https://baalajimaestro:${GH_PERSONAL_TOKEN}@github.com/MyPaperPlane/telegram-userbot.git
git fetch
git checkout staging
git pull origin staging
git push --force origin staging:master
tg_sendinfo "<code>I have merged all commits from staging into master</code>"
