# Telegram-UserBot

[![Build Status](https://semaphoreci.com/api/v1/baalajimaestro/telegram-userbot/branches/modular/badge.svg)](https://semaphoreci.com/baalajimaestro/telegram-userbot)

### If the semaphore build passed, but you still get syntax errors when running locally it's most probably not a problem with the source but with your version of python

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

# Contact
If you just want to stay in the loop about new features or
announcements you can join the [news channel](https://t.me/maestro_userbot_channel).

If you find any bugs or have any suggestions then don't hesitate to contact me in [my support group](https://t.me/userbot_support).

- This README is not guaranteed to always be up to date, refer to the [support channel](https://t.me/maestro_userbot_channel) for the latest informations.

## Dependencies:

- SQL DB, can be Postgres/MySQL or anything else supported by SQLAlchemy

- Neofetch (in case you need `sysdetails`)

### Before you start:
Get your api-id (called `API_KEY` in this bot) and API_HASH from my.telegram.org.


Optional: Create an empty group, add Marie, or any forks, get the group id, copy it and set it as your `LOGGER` (in case you want logging).


**Carfully read this entire guide before cloning so you don't end up getting stuck. When followed properly you'll end up with your userbot up and running after following it.**

#### Running on Heroku:
1. **Make sure to generate a session file, by running app.py on your local pc before deploying it on Heroku.**
- Fork this repo.
- Download/Clone it to your Linux PC, then follow the instructions on running on Linux below, to generate a userbot.session file, which is needed to run your bot.
> **A session is a key to your Telegram account, pushing it to GitHub will grant any person full access to your Telegram account.
You must be extra careful when pushing to GitHub. The gitignore in this repository should prevent this from happening in most cases, but you should still keep this in mind to prevent any fatal consequences.**
- You can choose bleeding edge builds which might be buggy, otherwise choose a release tags.
- If you use a bleeding edge, your bot version will be `b`
- Push it with the heroku cli
- Deploy.

#### Running on linux:
- Clone the repo: `git clone https://github.com/baalajimaestro/Telegram-UserBot`
- Checkout to the latest release tag incase you want a stable build, else you can go ahead with bleeding edge ones.
- `git tag -l #lists all versions available`
- `git checkout tags/version_number #replace version_number with your choice`
- Install all dependencies after moving to the project directory by running: `pip3 install -r requirements.txt`
- Configure your bot in `config.py` (You can use `sample_config.py` as a reference when doing so)
  - Remove the warning from sample_config, it is to prevent simple renaming and running
  - You can optionally use environment variables to configure it instead
- Start the userbot: `python3 -m userbot`

#### Running on Windows:

- Use the exclusive script provided
- Setup the config as in Linux
- Run `pip install telethon`
- Start the bot by using `python3 windows_startup_script.py`

### Commands available(might go horribly out-of-date anytime):

> `.` stands for any random character, it is made for the ease of the user

#### Utilities
- `.approvepm`: approve DMing
- `.iamafk`: Sets you as AFK
- `.notafk`: Sets you as not AFK, and gives you brief list if who messaged you while you were away
- `.addfilter trigger response`: Adds a filter in that group, if text is contained in incoming message, bot replies with the reply
- `.nofilter trigger`: removes the filter text from the current group
- `.rmfilters`: remove all filters
- `.get filters`: fetch all filters set in the userbot in that chat
- `.chatid`: show chat id
- `.userid`: show user id
- `.getqr`: encrypt QRCode
- `.screencapture`

#### Notes
- `.get notes`
- `.nosave`
- `.addnote`
- `.rmnotes`


#### Purge
- `.fastpurge`
- `.purgeme`
- `.delmsg`
- `.editme`
- `.sd`

#### Scraper:
- `.img`
- `.google`
- `.wiki`
- `.ud`
- `.tts`
- `.trt`: translate text
- `.lang`: change language

#### Admin Commands:
- `.wizard`: promote user
- `.thanos`: ban user
- `.spider`: mute user
- `.speak`: unmute user

#### MISC
- `.pip`
- `.pingme`: pings server
- `.paste`: paste code in hastebin
- `.log`
- `.log silent`: logs the message but silently
- `.speed`: speed test
- `.hash`
- `.random`
- `.alive`: check if bot is running
- `.restart`: restart the bot
- `.shutdown`: shutdown the bot
- `.real_shutdown`: REALLY shutdown the bot
- `.support`: get support
- `.supportchannel`: get support
- `.repo`: show the repo
- `.sysdetails`
- `.botversion`
- `.term`: execute terminal commands

#### MEMES(much are kanged from SkittBot)
- `:/`
- `-_-`
- `.cp`
- `.vapor`
- `.str`
- `.zal`
- `.owo`
- `.react`
- `.shg`: ¯\_(ツ)_/¯
- `.runs`: random message
- `.disable runs`
- `.enable runs`
- `.mock`


### Credits:

I would like to thank people who assisted me throughout this project:

* [@YouTwitFace](https://github.com/YouTwitFace)
* [@TheDevXen](https://github.com/TheDevXen)
* [@Skittles9823](https://github.com/Skittles9823)
* [@deletescape](https://github.com/deletescape)
* [@songotenks69](https://github.com/songotenks69)
* [@Ovenoboyo](https://github.com/Ovenoboyo)
* [SphericalKat](https://github.com/ATechnoHazard)

and many more people which aren't mentioned here.

Found Bugs? Create an issue on the issue tracker, or post it in the support group.
