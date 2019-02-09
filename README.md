# Telegram-UserBot

 [![Build Status](https://travis-ci.com/baalajimaestro/Telegram-UserBot.svg?branch=modular)](https://travis-ci.com/baalajimaestro/Telegram-UserBot) [![codecov](https://codecov.io/gh/baalajimaestro/Telegram-UserBot/branch/modular/graph/badge.svg)](https://codecov.io/gh/baalajimaestro/Telegram-UserBot)

 #### To track Semaphore builds, see the commits section. Since I use Semaphore 2.0, it is not possible to track the progress fully, or put a badge here. Ignore Travis CI for PRs.


### If the CI builds pass, but you still get syntax errors when running locally it's most probably not a problem with the source but with your version of python


```diff
- #include <std/disclaimer.h>
- /
- Your Telegram account may get banned.
- I am not responsible for any improper use of this bot
- This bot is intended for the purpose of having fun with memes
- as well as efficiently managing groups
- You ended up spamming groups, getting reported left and right,
- and the Telegram Team deleted your account?
- And then you pointed your fingers at me for getting yourself reported?
- I will laugh at you.
- /
```

A modular telegram Python UserBot running on python3 with an sqlalchemy database.

Started up as a simple bot, which helps with deleting messages and other stuffs when I didn't possess a smartphone(selecting each message indeed difficult) with a ton of meme features kanged from [SkittBot](https://github.com/skittles9823/SkittBot), it has evolved, becoming extremely modular and simple to use.


If you just want to stay in the loop about new features or
announcements you can join the [news channel](https://t.me/maestro_userbot_channel).

If you find any bugs or have any suggestions then don't hesitate to contact me in [my support group](https://t.me/userbot_support).

- This README is not guaranteed to always be up to date, refer to the [support channel](https://t.me/maestro_userbot_channel) for the latest informations.

## Getting your own userbot up and running:

**Carefully read this entire guide before cloning so you don't end up getting stuck. When followed properly you'll end up with your userbot up and running after following it.**

## A big note for humans : Please don't push your config.env and userbot.session to GitHub directly, Please, can you not

## Automated Method:


- `curl -sLo init_script.sh https://raw.githubusercontent.com/baalajimaestro/Telegram-UserBot/modular/init/init_script.sh`

- `bash init_script.sh`


## Manual Method:


### Before you start:

Clone this repo `git clone https://github.com/baalajimaestro/Telegram-UserBot`

Pip install all the requirements, `pip3 install -r requirements.txt`

Get your api-id (called `API_KEY` in this bot) and API_HASH from my.telegram.org.

Install all the requirements by running `pip3 install -r requirements.txt`

Optional: Create an empty group, add Marie, or any forks, get the group id, copy it and set it as your `LOGGER` (in case you want logging).

### Database

If you wish to use a database-dependent module (eg: locks, notes, userinfo, users, filters, welcomes),
you'll need to have a database installed on your system. I use postgres, so I recommend using it for optimal compatibility.

In the case of postgres, this is how you would set up a the database on a debian/ubuntu system. Other distributions may vary.

- install postgresql:

`sudo apt-get update && sudo apt-get install postgresql`

- change to the postgres user:

`sudo su - postgres`

- create a new database user (change YOUR_USER appropriately):

`createuser -P -s -e YOUR_USER`

This will be followed by you needing to input your password.

- create a new database table:

`createdb -O YOUR_USER YOUR_DB_NAME`

Change YOUR_USER and YOUR_DB_NAME appropriately.

- finally:

`psql YOUR_DB_NAME -h YOUR_HOST YOUR_USER`

This will allow you to connect to your database via your terminal.
By default, YOUR_HOST should be 127.0.0.1:5432.

You should now be able to build your database URI. This will be:

`sqldbtype://username:pw@hostname:port/db_name`

Replace sqldbtype with whichever db youre using (eg postgres, mysql, sqllite, etc)
repeat for your username, password, hostname (localhost?), port (5432?), and db name.


### Configuration:

There are two possible ways of configuring your bot: a config.env file, or ENV variables.

The prefered version is to use a `config.env` file, as it makes it easier to see all your settings grouped together.
This file should be placed in the topmost part of the repo.
This is where your `API KEYS` will be loaded from, as well as your `database URI` (if you're using a database), and most of
your other settings.

An example `config.env` file could be:
```
    API_KEY=123456
    BUILD_CHOICE="bleeding"
    API_HASH='4588acb1863ead924119c885dfffba2'
    LOGGER_GROUP=-1001200493567
    LOGGER=True    #Incase you want to turn off logging, put this to false
    TRT_ENABLE=False
    PM_AUTO_BAN=True
    CONSOLE_LOGGER_VERBOSE=True
    SCREEN_SHOT_LAYER_ACCESS_KEY="get from screenshot layer website google it "
    OPEN_WEATHER_MAP_APPID="get it from openweather site"
    DB_URI="postgres://userbot:mypass@localhost:5432/userbot"
```

If you can't have a config.env file, or you missed to type something on `config.env` but then pushed it up, it is also possible to use environment variables.


## Starting the bot.

Once you've setup your database and your configuration (see below) is complete, simply run:

`python3 -m userbot`


### Running on Termux:

Userbot setup on termux:

- **REQUIRED:**

`pkg install clang curl python python-dev postgresql-dev libcrypt-dev libffi-dev openssl-dev libxml2-dev libxslt-dev libjpeg-dev libjpeg-turbo-dev ndk-sysroot make`

- **OPTIONAL (Only if you are not planning to use any external DB. Also you can omit this if you don't plan of using a DB at all)**

`pg_ctl -D $PREFIX/var/lib/postgresqlstart`


`createdb <DBNAME>`


`createuser <USER>`


`psql <DBNAME> -h 127.0.0.1 <USER>`

- **Installing Requirements:** `pip3 install -r requirements.txt`

- **Finally Run it now:** `python3 -m userbot`


#### Running on Heroku:

1. **Make sure to generate a session file, by running app.py on your local pc/Termux before deploying it on Heroku.**

For using Heroku CLI on termux, please Google on it.
- Make sure you followed the instruction to setup the config file/ENV variables.
- If you need Database Commands, provision a heroku postgres instance.
- Push you bot along with `config.env` and `userbot.session` with the heroku cli, you need `git add -f` to add both of them.
- Deploy.


### Available Commands on readme have been removed due to non-maintainability. It follows marie syntax, replace all ! and / with a .

#### Special ones to take a note of:

`.google`
`.wiki`
`.img`
`.ud`
`.spam n text` (Dont use this tho)
`.purgeme n` (Purges your n messages)
`.afk`
`.ppic`
`.term`
`.exec`
`.eval`
`.upload`
`.download`
`.getqr`

### Creating your own modules.

Creating a module has been simplified as much as possible - but do not hesitate to suggest further simplification.

All that is needed is that your .py file be in the modules folder.

To add commands, make sure to import the the primary bot via

`from userbot import bot`.


and


telethon's important stuff via

`from telethon import events`

You can then add commands wrapping them under

```
@bot.on(events.NewMessage(outgoing=True,pattern=""))
async def some_function(e):
     Whatever here.
```


You can also set outgoing to incoming incase, you wanna make that command to parse the incoming message.

The command pattern will be regex. Hope you know it, else feel free to hop on [here](https://regexone.com)

Use asynchronous functions, and await the functions.

Should you need assistance with telethon library check out their [documentation](http://telethon.readthedocs.io/) or get support from [them](https://t.me/TelethonChat)


### Credits:

I would like to thank people who assisted me throughout this project:

* [@YouTwitFace](https://github.com/YouTwitFace)
* [@TheDevXen](https://github.com/TheDevXen)
* [@Skittles9823](https://github.com/Skittles9823)
* [@deletescape](https://github.com/deletescape)
* [@songotenks69](https://github.com/songotenks69)
* [@Ovenoboyo](https://github.com/Ovenoboyo)
* [SphericalKat](https://github.com/ATechnoHazard)
* [nitamarcel](https://github.com/nitanmarcel)

and many more people who aren't mentioned here.

Found Bugs? Create an issue on the issue tracker, or post it in the [support group](https://t.me/userbot_support).
