# Telegram-UserBot 

Just coz I'm too lazy, I program it, to make stuff easier.
This is a userbot, which is equivalent to a telegram client, and it can run on the cloud too.

# Contact 
Join the [news channel](https://t.me/maestro_userbot_channel) if you just want to stay in the loop about new features or
announcements.

If you found any bugs or you wanna suggest some features then contact [My support group](https://t.me/userbot_support).

Alternatively, [find me on telegram](https://t.me/baalajimaestro)!.

### Before you start:
Get your api-id(API_KEY in my code), API_HASH from my.telegram.org.<br/><br/>
**Please read through this before cloning. I don't want you get stuck anywhere. This guide can get you running up the userbot, if followed properly**

#### Running on heroku:
```diff
-If you clone/fork this repo please make sure you generate a session file  by running app.py on your local pc before deploying it on heroku.

- If you get errors like -->app[worker.1]: telethon.errors.rpcerrorlist.AuthKeyDuplicatedError: An auth key with the same ID was already generated, 

- It means your session was banned and needs to be regenerated.
```

- Fork my repo.

- Download/Clone it in your linux PC, then follow instructions on Running on linux(below), this will generate a session_name.session file, which is needed to run your bot, push this file to your git.

- Connect your git to heroku.

- Add API_KEY and API_HASH in CONFIG VARS. 

- Deploy.

#### Running on linux:
- Clone my repo: `git clone https://github.com/baalajimaestro/Telegram-UserBot`

- Install the necessary dependencies by moving to the project directory and running: `pip3 install -r requirements.txt`

- Add your API_KEY and API_HASH: `export API_HASH=your-api-hash` and `export API_KEY=your-api-id`

- Start the userbot: `python3 app.py`

### Commands available(incomplete):
 - `.delmsg`:                      Deletes the last typed message
 
 - `.purgeme number`:              Deletes last n messages sent by you
 
 - `.vapor`:                       Change the font to an aesthetic font.
 
 - `.cp`:                          CopyPasta, as in SkittlesBot
 
 - `.trt`:                         Google Translator, translates only to english
 
 - `.thanos`:                      Bans a person from the group
 
 - `.spider`:                      Mutes a person in the group if you are an admin
 
 - `.wizard`:                      In beta stage, needs all admin rights to work
 
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
 
 - `.help`:                        Get a link to this readme
 
 - `.killme(incoming)`:            If your bot senses it, it will reply a funny message, try it out
 
 - `.paste string`:                Sends the string to hastebin and gets the link
    
 - `.asmon n`:                     Turns on Anti-Spam Handler to mute a person on group for 2d, if 'n' messages exceeded 
 
 - `.asmoff`:                      Turns off the Anti-Spam Handler
 
 - `.term command`:                Executes a terminal command(Linux if heroku)
 
 - `.bigspam`:                     For huge spams like 1k
 
Clone this and try to add features to it, make pull requests to merge it ;) 
