#!/usr/bin/env sh

clear
echo "*****Welcome to baalajimaestro's userbot setup*****
This Guided Setup shall help you get your own userbot up and running.
You might be asked for sudo password several number of times."

if [ "$(lsb_release -is)" = "Ubuntu" ]; then
    sudo add-apt-repository ppa:deadsnakes/ppa
fi

sudo apt --yes --force-yes upgrade
    sudo apt --yes --force-yes install build-essential checkinstall git \
    libreadline-gplv2-dev libncursesw5-dev libssl-dev wget \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
    sudo apt --yes --force-yes install python3.7

sudo useradd userbot
    echo "userbot ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers
clear

cd /tmp || exit
    git clone https://github.com/baalajimaestro/Telegram-UserBot
        cd Telegram-UserBot || exit

read -r "Press y to go ahead with bleeding builds. Or press any other key for stable " BUILDS

if [ "$BUILDS" != "y" ]; then
    X=git tag -l | cut -f 1 | tail -n 1
    git checkout tags/"$X"
    clear
fi

echo "***Installing Requirements***"
sudo python3.7 -m pip install -r requirements.txt
    curl -sLo bot https://raw.githubusercontent.com/baalajimaestro/Telegram-UserBot/modular/init/userbot
clear

echo "***Please enter your details***"
read -r "What's your API_ID? " API_KEY
read -r "What's your API_HASH? " API_HASH
read -r "What's your Screenshot Layer API Key? " SCREENSHOT_LAYER_ACCESS_KEY
read -r "Do you need PMPermit Enabled? (y/n) " PMPERMIT
read -r "Do you need Logging Enabled? (y/n) " LOG
read -r "What's your OpenWeatherMap API Key? " OPEN_WEATHER_MAP_APPID
read -r "Do you need a Database Mode? (y/n) " DB

if [ "$PMPERMIT" = "y" ]; then
    PM_AUTO_BAN=True
else
    PM_AUTO_BAN=False
fi

if [ "$LOG" = "y" ]; then
    read -r "Enter the Log Group ID: " LOGGER_GROUP
    LOGGER=True
else
    LOGGER=False
    LOGGER_GROUP=0
fi

if [ "$DB" = "y" ]; then
    read -r "Enter your DB URL: " DB_URI
else
    DB_URI=None
fi

echo "API_KEY=$API_KEY
API_HASH=$API_HASH
SCREENSHOT_LAYER_ACCESS_KEY=$SCREENSHOT_LAYER_ACCESS_KEY
PM_AUTO_BAN=$PM_AUTO_BAN
LOGGER=$LOGGER
LOGGER_GROUP=$LOGGER_GROUP
OPEN_WEATHER_MAP_APPID=$OPEN_WEATHER_MAP_APPID
DB_URI=$DB_URI" >> config.env

python3.7 -m userbot test
sudo mv bot /etc/systemd/system/userbot.service
sudo chown -R userbot /tmp/Telegram-UserBot
sudo chmod -R 777 /tmp/Telegram-UserBot
sudo systemctl start userbot.service
sudo systemctl enable userbot.service
echo "

Pushed to init.d. Bot must work on reboot too.

Hope you love using my bot."
exit
