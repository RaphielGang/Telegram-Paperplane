# Telegram-UserBot 

Just coz I'm too lazy, I program it, to make stuff easier.
This is a userbot, which is equivalent to a telegram client, and it can run on the cloud too.
It needs a linux pc or any unix to run basic commands, or you need to find the workaround yourself :/

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

- Push it with the heroku cli

- Deploy.

#### Running on linux:
- Clone my repo: `git clone https://github.com/baalajimaestro/Telegram-UserBot`

- Install the necessary dependencies by moving to the project directory and running: `pip3 install -r requirements.txt`

- Add your API_KEY, API_HASH and LOGGER, and other stuff to config.py(You need to create it, a sample is provided)

- Remove the warning provided in sample_config, it is to avoid just rename and leave cases

- Or you use them as ENV Variables, upto your ease

- Start the userbot: `python3 -m userbot`

### Commands available(will be constantly updated):

-----`.` stands for any random character, it is made for the ease of the user------

- `.delmsg`:                         Deletes the last typed message

- `.purgeme number`:                 Deletes last n messages sent by you

- `.vapor`:                          Change the font to an aesthetic font.

- `.cp`:                             CopyPasta, as in SkittlesBot

- `.trt`:                            Google Translator, translates to the language specified by lang

- `.thanos`:                         Bans a person from the group

- `.spider`:                         Mutes a person in the group if you are an admin

- `.wizard`:                         In beta stage, needs all admin rights to work

- `.react`:                          Sends a random ascii emote

- `.editme`:                         Edits the last sent message with the string in the parameter

- `.pingme`:                         Pings your server

- `.iamafk`:                         Sets you as AFK

- `.notafk`:                         Sets you as not AFK, and gives you brief list if who messaged you while you were away

- `.ud`:                             Query urban dictionary

- `.google`:                         Query Google

- `.wiki`:                           Query Wikipedia and get a summary

- `.sd`:                             Send a self-destructing message

- `.eval`:                           Evaluate the given expression

- `.fastpurge`:                      Purge like marie

- `.spam number string`:             Spams the string n times

- `.exec`:                           Execute a python command

- `.help`:                           Get a link to this readme

- `.killme(incoming)`:               If your bot senses it, it will reply a funny message, try it out

- `.paste string`:                   Sends the string to hastebin and gets the link

- `.asmon n`:                        Turns on Anti-Spam Handler to mute a person on group until anti-spam is turned off

- `.asmoff`:                         Turns off the Anti-Spam Handler

- `.term command`:                   Executes a terminal command(Linux if heroku)

- `.bigspam`:                        For huge spams like 1k

- `.random a,b,c`:                   Finds random of a,b,c

- `.base64 en|decode`:               Pretty explains it

- `.hash`:                           Returns the md5 hash

- `.filter text reply`:              Adds a filter in that group, if text is contained in incoming message, bot replies with the reply

- `.nofilter text`:                  Removes the filter text from the current group

- `.save text reply`:                It saves reply for the text, can be obtained with #text again.

- `.speak`:                          Unmutes a user

- `.get filters`:                    Fetch all filters set in the userbot in that chat

- `.get notes`:                      Fetch all notes set in the userbot in that chat

- `.img text`:                       Search and fetch first two images from google

- `.approvepm`:                      Approves the Person in reply to PM, incase PM-Permit is enabled


Found Bugs? Start up an issue on issue tracker, or feel free to post in my support group.
