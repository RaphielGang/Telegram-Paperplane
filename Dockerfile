FROM baalajimaestro/userbot_python:latest

ENV PATH="/app/bin:$PATH"
WORKDIR /app

RUN git clone https://github.com/RaphielGang/Telegram-UserBot.git -b master /app

#
# Install requirements just in case the Docker Image isn't updated
#
RUN pip install --upgrade -r requirements.txt

#
# Copies session and config(if it exists)
#
COPY ./userbot.session ./config.env* ./client_secrets.json* ./secret.json* /app/

#
# Finalization
#
CMD ["bash","init/start.sh"]
