FROM ashdroid4/docker:latest

ENV PATH="/app/bin:$PATH"
WORKDIR /app

RUN git clone https://github.com/ashdroid4/Telegram-Paperplane.git -b master /app

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* ./client_secrets.json* ./secret.json* /app/

#
# Finalization
#
CMD ["bash","init/start.sh"]
