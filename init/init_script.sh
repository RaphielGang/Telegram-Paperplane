#!/usr/bin/env dash

set -e

scr_dir=$(realpath $(dirname $0))
prog_f=$scr_dir/.progress

reset_prog() {
    if [ -f "$prog_f" ]; then
        echo "Cleaning: $prog_f"
        rm $prog_f
    fi
    echo "Al progress has been reset.. now u can re-run the script from start"
    exit
}

save_prog() {
echo "$1=y" >> $prog_f
}

#reset progress.. if user prompted
[ "$1" = "--reset" ] && reset_prog

#load progress... if any
[ -f "$prog_f" ] && source $prog_f

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
    echo "Cloning bot sources..."
    if [ -z "$bot_clone" ]; then
        git clone https://github.com/baalajimaestro/Telegram-UserBot -b staging
        save_prog "bot_clone"
    fi
    echo "DONE!!"
    cd Telegram-UserBot
}

# Requirement install function
reqinstall() {
    echo "***Installing Requirements***"
    if [ -z "$req" ]; then
        sudo python3.7 -m pip install -r requirements.txt
        clear
        save_prog "req"
    fi
    echo "DONE!!"
}

DB="n"

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

#Fixup the postgresql server
postgresconfig() {
    echo "PostgreSQL config..."
    if [ -z "$psql" ]; then
        TRACK = echo `ls /etc/postgresql`
        sudo mv init/pg_hba.conf  /etc/postgresql/$TRACK/main/pg_hba.conf
        sudo echo "listen_address = '*'" >> postgresql.conf
        save_prog "psql"
    fi
    echo "DONE!!"
}

# Config write function
writeconfig() {
    echo "Configuring..."
    if [ -z "$gen_conf" ]; then
    questions
    echo "API_KEY=$API_KEY
API_HASH=$API_HASH
SCREENSHOT_LAYER_ACCESS_KEY=$SCREENSHOT_LAYER_ACCESS_KEY
PM_AUTO_BAN=$PM_AUTO_BAN
LOGGER=$LOGGER
LOGGER_GROUP=$LOGGER_GROUP
OPEN_WEATHER_MAP_APPID=$OPEN_WEATHER_MAP_APPID
DATABASE_URL=$DB_URI" >> config.env
    sudo mv config.env ~/Telegram-UserBot
    save_prog "gen_conf"
    fi
    echo "DONE!!"
}

#Generate the userbot.session
session() {
    echo "Generating session..."
    if [ -z "$sess" ]; then
        python3 windows_startup_script.py
        python3.7 -m userbot test
        save_prog "sess"
    fi
    echo "DONE!!"
}

#Spinup Docker installation
dockerspin() {
    echo "Docker installation..."
    if [ -z "$dock" ]; then
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo chmod 777 /var/run/docker.sock
    cd ~/Telegram-UserBot
    docker build -t userbot .
    save_prog "dock"
    fi
    echo "DONE!!"
}

# Systemd service bringup
systemd() {
    echo "Sys service..."
    if [ -z "$sysserv" ]; then
        sudo mv userbot /etc/systemd/system/userbot.service
        save_prog "sysserv"
    fi
    sudo systemctl start userbot.service
    sudo systemctl enable userbot.service
    echo "DONE!!"
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

writeconfig

if [ "$DB" = "y" ]
then
postgresconfig
fi
 
session
dockerspin

systemd
close
