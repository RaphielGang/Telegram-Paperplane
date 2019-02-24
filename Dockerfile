# We're using Alpine stable
FROM alpine:3.9

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

#
# Install all the required packages
#
RUN apk add --no-cache python3 \
    py-pillow py-requests py-sqlalchemy py-psycopg2 \
    curl neofetch git sudo gcc musl-dev postgresql postgresql-dev
RUN apk add --no-cache sqlite
# Copy Python Requirements to /app

RUN  sed -e 's;^# \(%wheel.*NOPASSWD.*\);\1;g' -i /etc/sudoers
RUN adduser userbot --disabled-password --home /home/userbot
RUN adduser userbot wheel
USER userbot
WORKDIR /home/userbot/userbot
COPY ./requirements.txt /home/userbot/userbot
#
# Install requirements
#
RUN sudo pip3 install -r requirements.txt
#
# Copy bot files to /app
#
COPY . /home/userbot/userbot
RUN sudo chown -R userbot /home/userbot/userbot
RUN sudo chmod -R 777 /home/userbot/userbot
cmd ["python3","-m","userbot"]
