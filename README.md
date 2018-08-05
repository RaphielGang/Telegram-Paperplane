# Telegram-UserBot [![Build Status](https://semaphoreci.com/api/v1/baalajimaestro/telegram-userbot/branches/master/badge.svg)](https://semaphoreci.com/baalajimaestro/telegram-userbot)

Just coz I'm too lazy, I program it, to make stuff easier.
This is a userbot, which is equivalent to a telegram client, and it can run on the cloud too.

### Before you start:
Get your api-id(API_KEY in my code), API_HASH from my.telegram.org.

#### Running on heroku:
<b>If you clone/fork this repo please make sure you delete session_name.session and regenerate it by running app.py on your local pc before deploying it on heroku.</b>

- Fork my repo.

- Download/Clone it in your linux PC, then follow instructions on Running on linux(below), this will generate a session_name.session file, which is needed to run your bot, push this file to your git.

- Connect your git to heroku.

- Add API_KEY and API_HASH in CONFIG VARS. 

- Deploy.

#### Running on linux:
- Clone my repo: `git clone https://github.com/shanuflash/userbot`

- Add your API_KEY and API_HASH: `export API_HASH=your-api-hash` and `export API_KEY=your-api-id`

- Start the userbot: `python3 app.py`

### Commands available(incomplete):
 - `.delmsg`:                      Deletes the last typed message
 
 - `.purgeme number`:              Deletes last n messages sent by you
 
 - `.vapor`:                       Change the font to an aesthetic font.
 
 - `.cp`:                          CopyPasta, as in SkittlesBot
 
 - `.trt`:                         Google Translator, translates only to english
 
 - `.tts`:                         Google Text to Speech
 
 - `.react`:                       Sends a random ascii emote
 
 - `.editme`:                      Edits the last sent message with the string in the parameter
 
 - `.pingme`:                      Pings you
 
 - `.iamafk`:                      Sets you as AFK
 
 - `.notafk`:                      Sets you as not AFK, and gives you brief list if who messaged you while you were away
 
 - `.ud`:                          Query urban dictionary
 
 - `.google`:                      Query Google
 
 - `.wiki`:                        Query Wikipedia and get a summary
 
 - `.sd`:                          Send a self-destructing message
 
 - `.eval`:                        Evaluate the given expression
 
 - `.fastpurge`:                   Purge like marie
 
 - `.spam number string`:          Spams the string n times
 
 - `.exec`:                        Execute a python command
    
Clone this and try to add features to it, make pull requests to merge it ;) 
