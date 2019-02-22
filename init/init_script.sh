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

# Clone the required repo
botclone() {
    cd ~
    git clone https://github.com/baalajimaestro/Telegram-UserBot -b staging
    cd Telegram-UserBot
}

# Requirement install function
reqinstall() {
    echo "***Installing Requirements***"
    sudo python3.7 -m pip install -r requirements.txt
    curl -sLo bot https://raw.githubusercontent.com/baalajimaestro/Telegram-UserBot/modular/init/userbot
    clear
}
DB = "n"
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

#Fixup the poatgresql server
postgresconfig() {
TRACK = echo `ls /etc/postgresql`
sudo mv init/pg_hba.conf  /etc/postgresql/$TRACK/main/pg_hba.conf
sudo echo "listen_address = '*'" >> postgresql.conf
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
sudo mv config.env ~/Telegram-UserBot
}

#Generate the userbot.session
session() {
python3.7 -m userbot test
}
#Spinup Docker installation
dockerspin() {
sudo systemctl start docker
sudo systemctl enable docker
sudo chmod 777 /var/run/docker.sock
cd ~/Telegram-UserBot
docker build -t userbot .
}
# Systemd service bringup
systemd() {
    sudo mv bot /etc/systemd/system/userbot.service
    sudo systemctl start userbot.service
    sudo systemctl enable userbot.service
}

# Close down
close() {
    echo "

Pushed to systemd service. Bot runs on docker, and it will run across reboots too.

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

reqinstall

questions
writeconfig

if [ "$DB" = "y" ]
then
postgresconfig
fi
 
session
dockerspin

systemd
close
