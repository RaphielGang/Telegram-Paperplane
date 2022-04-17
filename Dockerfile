FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
	git \
	curl \
	sudo \
	libwebp-dev \
	redis \
	neofetch \
	libssl-dev \
	libjpeg-dev \
	jq \
	pv

ENV PATH="/usr/src/app/bin:$PATH"
WORKDIR /usr/src/app

RUN git clone https://github.com/RaphielGang/Telegram-UserBot.git -b master ./

RUN pip install -r requirements.txt


#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* ./client_secrets.json* ./secret.json* ./spotify_session* ./

#
# Finalization
#
CMD ["bash","init/start.sh"]
