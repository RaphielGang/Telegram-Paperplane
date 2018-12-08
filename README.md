# Telegram-UserBot 

[![Build Status](https://semaphoreci.com/api/v1/baalajimaestro/telegram-userbot/branches/modular/badge.svg)](https://semaphoreci.com/baalajimaestro/telegram-userbot)

### If you see the semaphore badge showing passed, still running on your local PC gives syntax it must be very clear that it isn't a problem with the source, you need to check your compiler

```diff
- #include <std/disclaimer.h>
- /
- Your Telegram account may be banned.
- I am not responsible for improper use of this bot
- This bot is to have fun memes
- Manage group in an efficient manner
- Ending up spamming in groups, getting reported, and Telegram Team deleted your account?
- And then you point the finger at me for getting yourself reported?
- I will laugh at you, because thats gay af
- /
```

# Contact 
Join the [news channel](https://t.me/maestro_userbot_channel) if you just want to stay in the loop about new features or
announcements.

If you found any bugs or you wanna suggest some features then contact [My support group](https://t.me/userbot_support).

- This Readme might go out-of-date at any point, as I push notifications for all updates to my [support channel](https://t.me/maestro_userbot_channel). I recommend subscribing to the channel, for timely updates and fixes.

## Dependencies:

- SQL DB, Can be Postgres/MySQL or anything, basically the bot uses SQLAlchemy

- Neofetch(in case you need sysdetails)

### Before you start:
Get your api-id(API_KEY in my code), API_HASH from my.telegram.org.<br/><br>
Create an empty group, add marie, or any of its clone, find group id, then copy it and this is your LOGGER(Incase you want logging) It can be very well turned off<br/><br/>
**Please read through this before cloning. I don't want you get stuck anywhere. This guide can get you running up the userbot, if followed properly**

#### Running on heroku:
```diff
-If you clone/fork this repo please make sure you generate a session file  by running app.py on your local pc before deploying it on heroku.
```

- Fork my repo.

- Download/Clone it in your linux PC, then follow instructions on Running on linux(below), this will generate a userbot.session file, which is needed to run your bot.

- You can choose bleeding edge builds which might be buggy, else can choose from release tags.

- If you use a bleeding edge, your botversion will bear `b` on the botversion

##### The session is the key to your telegram account, pushing it to github will grant any person access to your telegram account.
#####  You must be extra careful when you push to github. Though my gitignore avoids session files, I am still notifying this,
#####  coz it causes serious consequences if the session reaches the wrong hands

- Push it with the heroku cli

- Deploy.

#### Running on linux:
- Clone my repo: `git clone https://github.com/baalajimaestro/Telegram-UserBot`

- Install the necessary dependencies by moving to the project directory and running: `pip3 install -r requirements.txt`

- Add your API_KEY, API_HASH and LOGGER, and other stuff to config.py(You need to create it, a sample is provided)

- Remove the warning provided in sample_config, it is to avoid just rename and leave cases

- Or you use them as ENV Variables, upto your ease

- Start the userbot: `python3 -m userbot`

#### Running on Windows: 

- Use the exclusive script provided

- Setup the config as in linux

- Pip install just telethon

- Start the bot `python3 windows_startup_script.py`

### Commands available(might go horribly out-of-date anytime):

-----`.` stands for any random character, it is made for the ease of the user------

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
- `.speed`: speed test
- `.hash`
- `.random`
- `.alive`: check if bot is running
- `.restart`: restart the bot
- `.shutdown`: shutdown the bot
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

[@YouTwitFace](https://github.com/YouTwitFace)<br/>
[@TheDevXen](https://github.com/TheDevXen)<br/>
[@Skittles9823](https://github.com/Skittles9823)<br/>
[@deletescape](https://github.com/deletescape)<br/>
[@songotenks69](https://github.com/songotenks69)<br/>
[@Ovenoboyo](https://github.com/Ovenoboyo)<br/>
[SphericalKat](https://github.com/ATechnoHazard)<br/>
<br/>
and much more people I haven't mentioned here too.

Found Bugs? Start up an issue on issue tracker, or feel free to post in my support group.
