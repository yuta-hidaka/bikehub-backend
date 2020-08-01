FROM nginx/unit:1.14.0-python3.7
ARG APP_NAME
ARG APP_PORT
WORKDIR /code
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /code/
RUN apt-get update -y&&\
    apt-get upgrade -y&&\
    apt-get install mecab libmecab-dev \
    mecab-ipadic mecab-ipadic-utf8 sudo python3 python3-pip\
    git make curl xz-utils file -y&&\
    git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git&&\
    /code/mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y &&\
    mkdir /code/media && \
    mkdir /code/static &&\
    python3 -m pip3 install --upgrade pip3 &&\
    pip3 install -r requirements.txt &&\
    rm /code/config.json || echo 'skip rm /code/config.json' && \
    touch /code/config.json &&\
    echo  '                                                   \
    {                                                           \
        "listeners": {                                          \
            "*:${APP_PORT}": {                                  \
            "pass": "applications/app"                          \
            }                                                   \
        },                                                      \
                                                                \
        "applications": {                                       \
            "app": {                                            \
                "type": "python",                               \
                "processes": 2,                                 \
                "path": "/usr/code/${APP_NAME}/",               \
                "module": "run"                                 \
            }                                                   \
        }                                                       \
    }                                                           \
    ' > /code/config.json

COPY . /code/
