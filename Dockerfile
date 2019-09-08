FROM baalajimaestro/userbot_python:latest

ENV PATH="/app/bin:$PATH"
WORKDIR /app

RUN git clone https://github.com/RaphielGang/Telegram-UserBot.git -b master /app

#
# Copies session and config(if it exists)
#
COPY ./userbot.session ./config.env* ./client_secrets.json* ./secret.json* /app

#
# Finalization
#
RUN mkdir /app/bin
RUN curl https://raw.githubusercontent.com/yshalsager/megadown/master/megadown -o /app/bin/megadown && sudo chmod a+x /app/bin/megadown
RUN curl https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py -o /app/bin/cmrudl && sudo chmod a+x /app/bin/cmrudl
CMD ["bash","init/start.sh"]
