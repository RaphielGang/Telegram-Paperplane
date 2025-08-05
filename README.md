# Paperplane userbot project

![logo](https://telegra.ph/file/73cf4c62b2c64f981961e.png)

```
#include <std/disclaimer.h>
/**
    Your Telegram account may get banned.
    We are not responsible for any improper use of Paperplane.
    Paperplane is intended for the purpose of effective group management,
    PM control as well as having fun with memes.
    You ended up spamming groups, getting reported left and right,
    and you ended up in a Finale Battle with Telegram and at the end
    Telegram Team deleted your account?
    And after that, then you pointed your fingers at us
    for getting your acoount deleted?
    We will be rolling on the floor laughing at you.
/**
```

## What is it?

Paperplane is a modular Telegram userbot running on Python3, which can be coupled up with MongoDB and a Redis backend to bring you features such as PMPermit (auto blocking strangers on PM), AFK messages, group management features (ban/mute/kick/etc, notes, filters, welcomes and so on), different scrapers making every daily and rare task easier, integration with different services and more! You can check the list of features with the `.help` command after installing Paperplane, or you can check the source code!

Originally created by baalajimaestro, Paperplane started as a simple userbot, with group management features inspired from Marie, memes from SkittBot and a ton of other modules. Paperplane has evolved to become a project with dozens of contributors. Paperplane is currently owned and maintained by [@zakaryan2004](https://github.com/zakaryan2004) as a side project, with the help of all contributors.

## How do I use it?

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NotAnyoneMe/Paperplane.git
   cd Paperplane
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot:**
   ```bash
   python setup.py
   ```

4. **Generate string session:**
   ```bash
   python generate_string_session.py
   ```

5. **Run locally:**
   ```bash
   python -m userbot
   ```

### Deployment Options

#### Deploy to Render (Recommended)
Render offers better reliability and Docker support compared to Heroku:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

📖 **[Complete Render Deployment Guide](RENDER_DEPLOYMENT.md)**

#### Deploy to Heroku (Legacy)
<p align="left"><a href="https://heroku.com/deploy?template=https://github.com/RaphielGang/Telegram-Paperplane"> <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" /></a></p>

### Prerequisites

- Python 3.9+
- Telegram API credentials from https://my.telegram.org
- MongoDB Atlas database (free tier available)
- Generated string session

## Groups and support

If you'd just like to know about new features, or announcements, you can join our [news channel](https://t.me/paperplanechannel).

For discussion, bug reporting, and help, you can join [our discussion group](https://t.me/tgpaperplane).

If you find a bug, don't hesitate to report it in our Telegram group or open an issue on this repository. As for unofficial
forks of Paperplane, we will only assist with issues affecting our central repository, found on [this repo](https://github.com/RaphielGang/Telegram-Userbot). So, before asking help for setting up the bot or reporting a bug you found, MAKE SURE you are using this repo, and not a fork you found somewhere else. You may get ignored if you ask for help with a fork.

## Credits

Over the years, Paperplane evolved thanks to the dozens of contributors who have contributed, large or small, to the project. Listing all of them here would be impossible, as even the person in the group who reported a small bug has made their share of contribution to the project. We thank all of our contributors who have done and are doing even the slightest for the project.

The code contributors can be found at the [Contributors](https://github.com/RaphielGang/Telegram-Paperplane/graphs/contributors) page.
This page will obviously not list all code contributions correctly, as some contributors attributed their commits with emails not associated with a GitHub account or maybe a guy just made a small snippet of code, posted it on the Internet and it got used by us, in Paperplane. Paperplane could of course not become what it is now without the dependencies, which you can find in the `requirements.txt` file in the root of the repo. We are thankful to everyone who made Paperplane better.
