# We're using Alpine stable
FROM alpine:edge

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

# Installing Python 
RUN apk add --no-cache --update \
    git \
    bash \
    libffi-dev \
    openssl-dev \
    bzip2-dev \
    zlib-dev \
    readline-dev \
    sqlite-dev \
    build-base \
    python3

RUN python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache


#
# Install all the required packages
#
RUN apk --no-cache add build-base

RUN apk add --no-cache \
    py-pillow py-requests \
    py-sqlalchemy py-psycopg2 git py-lxml \
    libxslt-dev py-pip libxml2 libxml2-dev \
    libpq postgresql-dev \
    postgresql build-base linux-headers \
    jpeg-dev curl neofetch git sudo \
    gcc python-dev python3-dev \
    postgresql postgresql-client php-pgsql \
    musl postgresql-dev py-tz py3-aiohttp
RUN apk add --no-cache sqlite figlet libwebp-dev

# Copy Python Requirements to /app
RUN git clone https://github.com/psycopg/psycopg2 psycopg2 \
&& cd psycopg2 \
&& python setup.py install

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
RUN sudo pip3 install -U pip
RUN sudo pip3 install -r requirementsDOCKER.txt
RUN sudo chown -R userbot /home/userbot/userbot
RUN sudo chmod -R 777 /home/userbot/userbot
CMD ["python3","-m","userbot"]
