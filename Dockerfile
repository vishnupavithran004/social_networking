FROM python:3.10.5-slim-buster

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev gcc netcat git build-essential libssl-dev


ENV SN_SERVICE=/home/social_networking
# set work directory


RUN mkdir -p $SN_SERVICE
RUN mkdir -p $SN_SERVICE/static

# where the code lives
WORKDIR $SN_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
# copy project
COPY requirements.txt $SN_SERVICE
RUN pip install -r requirements.txt
CMD ["/bin/bash"]
