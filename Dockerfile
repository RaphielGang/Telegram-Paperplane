# We're using Alpine stable
FROM alpine:3.9

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
    build-base

# Set Python version
ARG PYTHON_VERSION='3.8-dev'
# Set pyenv home
ARG PYENV_HOME=/root/.pyenv
# Note installing THROUGH THIS METHOD WILL DELAY DEPLOYING
# Install pyenv, then install python versions
RUN git clone --depth 1 https://github.com/pyenv/pyenv.git $PYENV_HOME && \
    rm -rfv $PYENV_HOME/.git

ENV PATH $PYENV_HOME/shims:$PYENV_HOME/bin:$PATH

RUN pyenv install $PYTHON_VERSION
RUN pyenv global $PYTHON_VERSION
RUN pip install --upgrade pip && pyenv rehash

# Cleaning pip cache
RUN rm -rf ~/.cache/pip
#
# Install all the required packages
#
RUN apk --no-cache add build-base

RUN apk add --no-cache \
    py-pillow py-requests py-sqlalchemy py-psycopg2 git py-lxml \
    libxslt-dev py-pip libxml2 libxml2-dev libpq postgresql-dev \
    postgresql build-base linux-headers jpeg-dev \
    curl neofetch git sudo gcc python-dev python3-dev \
    postgresql postgresql-client php-pgsql \
    musl postgresql-dev
RUN apk add --no-cache sqlite
RUN adduser -D userbot
RUN echo "userbot ALL=ALL NOPASSWD: ALL" >> /etc/sudoers
USER userbot
#
RUN apk add figlet 
# Copy Python Requirements to /app
RUN git clone https://github.com/psycopg/psycopg2 psycopg2 \
&& cd psycopg2 \
&& python setup.py install

RUN  sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers
RUN adduser userbot --disabled-password --home /home/userbot
RUN adduser userbot wheel
USER userbot
WORKDIR /home/userbot/userbot
COPY ./requirementsDOCKER.txt /home/userbot/userbot
#
# Install requirements
#
RUN sudo pip3 install -U pip
RUN sudo pip3 install -r requirementsDOCKER.txt
#
# Copy bot files to /app
#
COPY . /home/userbot/userbot
RUN sudo chown -R userbot /home/userbot/userbot
RUN sudo chmod -R 777 /home/userbot/userbot
cmd ["python3","-m","userbot"]
