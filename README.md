# Paperplane Minimal Project

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

Clone this repo using `git clone https://github.com/HitaloSama/PaperplaneMinimal.git` and enter the newly created `PaperplaneMinimal` directory. Go ahead and open the directory.

Now install the requirements with

`python3 -m pip install -r requirements.txt`

This will install all the required dependencies. After this, you need to copy and expand the sample configuration file. Create a new file named `config.py` and make sure in the header you have `from sample_config import Config`. After that just copy the contents of the Config class in the `sample_config.py` file to your new file, fill in with your data and you should be done. You need your user API key and hash, you can get those in the [Telegram Core API](https://my.telegram.org/) website.

With these done, you should be ready to run your bot, follow the instructions in Starting up section. Good luck.

## Credits

Huge thanks to all [Contributors](https://github.com/HitaloSama/PaperplaneMinimal/graphs/contributors) who have helped make this userbot awesome!!

## Licensing

This project, is licensed under [Raphielscape Public License](https://github.com/HitaloSama/PaperplaneMinimal/blob/master/LICENSE), Version 1.d
