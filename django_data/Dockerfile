FROM python:3.6
WORKDIR /code
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /code/
RUN apt-get update -y&&\
    apt-get upgrade -y&&\
    apt-get install mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 sudo -y&&\
    apt-get install git make curl xz-utils file&&\
    git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git&&\
    /code/mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y &&\
    mkdir /code/media && \
    mkdir /code/static &&\
    python -m pip install --upgrade pip &&\
    pip install -r requirements.txt
COPY . /code/