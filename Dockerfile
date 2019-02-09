# We're using Alpine stable
FROM alpine:3.9

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' \
      -i /etc/apk/repositories

#
# Install all the required packages
#
RUN apk add --no-cache python3 \
    py-pillow py-requests py-sqlalchemy py-psycopg2 \
    curl neofetch git
RUN apk add --no-cache sqlite

#
# Copy Python Requirements to /app
#
COPY ./requirements.txt /app/
WORKDIR /app

#
# Install requirements
#
RUN pip3 install -r requirements.txt

#
# Copy bot files to /app
#
COPY . /app
cmd ["python3","-m","userbot"]
