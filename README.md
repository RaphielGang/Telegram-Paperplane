# Paperplane Minimal Project

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/651f0ed73d94478da6d783c480b60663)](https://app.codacy.com/manual/HitaloSama/PaperplaneMinimal?utm_source=github.com&utm_medium=referral&utm_content=HitaloSama/PaperplaneMinimal&utm_campaign=Badge_Grade_Dashboard)
[![Build](https://github.com/HitaloSama/PaperplaneMinimal/workflows/ErrorChecking/badge.svg?branch=master)](https://github.com/HitaloSama/PaperplaneMinimal/actions "Build") ![Contributors](https://img.shields.io/github/contributors/HitaloSama/PaperplaneMinimal?color=LightSlateGrey)  
[![@PaperplaneMinimal](https://img.shields.io/badge/%F0%9F%92%AC%20Telegram-%40PaperplaneMinimal-greem.svg)](https://telegram.me/PaperplaneMinimal)
[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/HitaloSama/PaperplaneMinimal/?ref=repository-badge)

![logo](https://telegra.ph/file/73cf4c62b2c64f981961e.png)

```
#include <std/disclaimer.h>
/**
    Your Telegram account may get banned.
    I am not responsible for any improper use of this bot
    This bot is intended for the purpose of having fun with memes,
    as well as efficiently managing groups.
    You ended up spamming groups, getting reported left and right,
    and you ended up in a Finale Battle with Telegram and at the end
    Telegram Team deleted your account?
    And after that, then you pointed your fingers at us
    for getting your acoount deleted?
    I will be rolling on the floor laughing at you.
/**
```

## What is

Paperplane Minimal is a minimalist fork of the Paperplane userbot, no database and only with modules that I (Hitalo) find useful and necessary for my use of Telegram.

## Getting started

Getting started is pretty easy, but a few commands currently rely on API access through a few different services, so be ready to sign up for some free accounts.
 
#### Step one
 
Clone this repo using `git clone https://github.com/HitaloSama/PaperplaneMinimal.git` and enter the newly created `PaperplaneMinimal` directory. Go ahead and open the directory in your favorite text editor, we're going to be doing some typing.
 
#### Step two
 
Copy `sample_config.env` to `config.env`. This file WILL NOT be checked into version control, so if you're hosting your bot remotely you'll need to think about that. Normal environment variables are also supported, but `config.env` makes things a little easier for local development at least.
 
Now open `config.env` in your text editor and remove the first two lines. If these aren't removed your file will not be loaded. For now the only variables we're going to change are the first two, `API_KEY` and `API_HASH`. Using your Telegram account information (ie. your phone number) login to https://my.telegram.org and click on the link that says API Development Tools. The `API_KEY` in your `config.env` will be the `APP api_id` and the  `API_HASH` will be the `APP api_hash`.
 
#### Step three
 
This bot includes logging for a lot of things, but to implement logging you need a chat for it to send logs to. Ideally this chat should NOT be a public chat with other people in it, or they will be getting spammed with logs (including some potentially semi sensitive information such as error logs).
 
You will need to get the chat id for the config file. The easiest way to do so would be to add [@MissRose_bot](https://t.me/MissRose_bot) to your group and send `/id`. Take the chat id and add it to your config file using the `BOTLOG_CHATID` environment variable.
 
To enable logging, set the `BOTLOG` environment variable to `True`.
 
#### Step four
 
Now it's time to generate a session with Telegram. This will allow us to maintain access to the Telegram API across restarts. First make sure all of the requirements are installed by running 
 
```
pip3 install -r requirements.txt --user
```
 
Once deps are installed we can generate a session file
 
```
python3 string_session.py
```
 
It will ask for your phone number, and then the code you get from Telegram. If you do everything right it should generate a `string_session`, copy it and put it in `config.env`.
 
1. DO NOT under any circumstances check `userbot.session` into version control or put it anywhere where someone else can get their hands on it.

#### Step five
 
We're almost done. Techincally your bot should work now, but there are some niceties that won't work until you provide an API key. You can skip this if you don't plan on using any of those. Don't worry, they're all free, check the `config.env` file to see the optional API and where to get them.
 
## Credits

Huge thanks to all [Contributors](https://github.com/HitaloSama/PaperplaneMinimal/graphs/contributors) who have helped make this userbot awesome!!

## Licensing

This project, is licensed under [Raphielscape Public License](https://github.com/HitaloSama/PaperplaneMinimal/blob/master/LICENSE), Version 1.d
