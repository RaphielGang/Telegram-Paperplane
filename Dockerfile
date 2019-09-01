# We're using Alpine Edge
FROM alpine:edge

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/edge/community;http\1/edge/community;g' -i /etc/apk/repositories

# Installing Core Components
RUN apk add --no-cache --update \
    git \
    bash \
    python3 \
    redis \   
    py-pillow \
    py-requests \
    libpq \
    curl \
    sudo \
    neofetch \
    musl \
    py-tz \
    py3-aiohttp \
    py-six \
    py-click

RUN python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

#
# Make user for userbot itself
#
RUN  sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers
RUN adduser userbot --disabled-password --home /home/userbot
RUN adduser userbot wheel
USER userbot

#
# Clone master by default
#
RUN git clone -b master https://github.com/RaphielGang/Telegram-UserBot.git /home/userbot/userbot

#
# !!! NOT FOR PRODUCTION !!!
# Copy Userbot components from Local
#
# COPY . /home/userbot/userbot

#
# Make binary folder and include in PATH
#
RUN mkdir /home/userbot/bin
ENV PATH="/home/userbot/bin:$PATH"
WORKDIR /home/userbot/userbot

#
# Copies session and config(if it exists)
#
COPY ./userbot.session ./config.env* ./client_secrets.json* ./secret.json* /home/userbot/userbot/

#
# Install dependencies
#
RUN pip3 install -r requirements.txt

#
# Finalization
#
RUN curl -s https://raw.githubusercontent.com/yshalsager/megadown/master/megadown -o /home/userbot/bin/megadown && sudo chmod a+x /home/userbot/bin/megadown
RUN curl -s https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py -o /home/userbot/bin/cmrudl && sudo chmod a+x /home/userbot/bin/cmrudl
CMD ["dash","init/start.sh"]
