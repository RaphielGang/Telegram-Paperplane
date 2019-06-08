# We're using Alpine stable
FROM alpine:edge

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

# Installing Python 
RUN apk add --no-cache --update \
    git \
    dash \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    build-base \
    python3 \
    redis \
    libxslt-dev \
    libxml2 \
    libxml2-dev \
    py-pip \
    libpq \
    build-base \
    linux-headers \
    jpeg-dev \
    curl \
    neofetch \
    sudo \
    gcc \
    python-dev \
    python3-dev \
    musl \
    sqlite \
    figlet \
    libwebp-dev

RUN pip3 install --upgrade pip setuptools

# Copy Python Requirements to /app

RUN  sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers
RUN adduser userbot --disabled-password --home /home/userbot
RUN adduser userbot wheel
USER userbot
RUN mkdir /home/userbot/userbot
RUN git clone -b master https://github.com/baalajimaestro/Telegram-UserBot /home/userbot/userbot
WORKDIR /home/userbot/userbot

#
#Copies session and config(if it exists)
#

COPY ./userbot.session ./config.env* /home/userbot/userbot/

#
# Install requirements
#

RUN sudo pip3 install -r requirements.txt
RUN sudo chmod -R 777 /home/userbot/userbot
CMD ["dash","init/start.sh"]