#!/usr/bin/env dash

# Welcome Message
welcome() {
    echo "*****Welcome to baalajimaestro's userbot setup*****
This Guided Setup shall help you get your own userbot up and running.
You might be asked for sudo password several number of times."
}

# Package requirements install
packageinstall() {
    # add-apt-repository only exists in Ubuntu
    [ "$(lsb_release -is)" = "Ubuntu" ] && sudo add-apt-repository ppa:deadsnakes/ppa

    sudo apt --yes --force-yes upgrade
    sudo apt --yes --force-yes install build-essential checkinstall git \
        libreadline-gplv2-dev libncursesw5-dev libssl-dev wget \
        libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
    sudo apt --yes --force-yes install python3.7 docker
}

# Create userbot user
createuser() {
    sudo useradd --create-home --home /home/userbot userbot
    echo "userbot ALL=(ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers
    clear
}

# Clone the required repo
botclone() {
    sudo -Hu userbot git clone https://github.com/baalajimaestro/Telegram-UserBot
    cd Telegram-UserBot || exit
}

# Requirement install function
reqinstall() {
    echo "***Installing Requirements***"
    sudo python3.7 -m pip install -r requirements.txt
    sudo -Hu userbot curl -sLo bot https://raw.githubusercontent.com/baalajimaestro/Telegram-UserBot/modular/init/userbot
    clear
}

# Questionaire
questions() {
    echo "***Please enter your details***"
    read -r -p "What's your API_ID? " API_KEY
    read -r -p "What's your API_HASH? " API_HASH
    read -r -p "What's your Screenshot Layer API Key? " SCREENSHOT_LAYER_ACCESS_KEY

    read -r -p "Do you need PMPermit Enabled? (y/n) " PMPERMIT
    if [ "$PMPERMIT" = "y" ]; then
        PM_AUTO_BAN=True
    else
        PM_AUTO_BAN=False
    fi

    read -r -p "Do you need Logging Enabled? (y/n) " LOG
    if [ "$LOG" = "y" ]; then
        read -r -p "Enter the Log Group ID: " LOGGER_GROUP
        LOGGER=True
    else
        LOGGER=False
        LOGGER_GROUP=0
    fi
    read -r -p "What's your OpenWeatherMap API Key? " OPEN_WEATHER_MAP_APPID

    read -r -p "Do you need a Database Mode? (y/n) " DB
    if [ "$DB" = "y" ]; then
        read -r -p "Enter your DB URL: " DB_URI
    else
        DB_URI=None
    fi
}

# Checkout to latest tag
checkout() {
    read -r -p "Press y to go ahead with bleeding builds. Or press any other key for stable " BUILDS
    rel=$(git tag -l | cut -f 1 | tail -n 1)
    [ "$BUILDS" != "y" ] && git checkout tags/"$rel"
    clear
}

# Config write function
writeconfig() {
    echo "API_KEY=$API_KEY
API_HASH=$API_HASH
SCREENSHOT_LAYER_ACCESS_KEY=$SCREENSHOT_LAYER_ACCESS_KEY
PM_AUTO_BAN=$PM_AUTO_BAN
LOGGER=$LOGGER
LOGGER_GROUP=$LOGGER_GROUP
OPEN_WEATHER_MAP_APPID=$OPEN_WEATHER_MAP_APPID
DB_URI=$DB_URI" >> config.env
sudo mv config.env /home/userbot/Telegram-UserBot 
sudo chown userbot /home/userbot/Telegram-Userbot/config.env
}

# Systemd service bringup
systemd() {
    sudo mv bot /etc/systemd/system/userbot.service
    sudo chown -R userbot /tmp/Telegram-UserBot
    sudo chmod -R 777 /tmp/Telegram-UserBot
    sudo systemctl start userbot.service
    sudo systemctl enable userbot.service
}

# Close down
close() {
    echo "

Pushed to init.d. Bot must work on reboot too.

Hope you love using my bot."
    exit
}

#
# Here's where the mejik happens
#
clear
welcome

createuser
cd /tmp || exit
botclone

checkout
reqinstall

questions
writeconfig

python3.7 -m userbot test
systemd
close
