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
    py3-pillow \
    py3-requests \
    libpq \
    curl \
    sudo \
    neofetch \
    musl \
    py3-tz \
    py3-aiohttp \
    py3-six \
    py3-click \
    py3-psutil \
    py3-lxml

RUN python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# Clone master by default
#
RUN git clone -b master https://github.com/RaphielGang/Telegram-UserBot.git /root/userbot

#
# !!! NOT FOR PRODUCTION !!!
# Copy Userbot components from Local
#
# COPY . /root/userbot

#
# Make binary folder and include in PATH
#
RUN mkdir /root/userbot/bin
ENV PATH="/root/userbot/bin:$PATH"
WORKDIR /root/userbot/

#
# Copies session and config(if it exists)
#
COPY ./userbot.session ./config.env* ./client_secrets.json* ./secret.json* /root/userbot/

#
# Install dependencies
#
RUN pip3 install -r requirements.txt

#
# Finalization
#
RUN curl -s https://raw.githubusercontent.com/yshalsager/megadown/master/megadown -o /root/userbot/bin/megadown && sudo chmod a+x /root/userbot/bin/megadown
RUN curl -s https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py -o /root/userbot/bin/cmrudl && sudo chmod a+x /root/userbot/bin/cmrudl
CMD ["bash","init/start.sh"]
