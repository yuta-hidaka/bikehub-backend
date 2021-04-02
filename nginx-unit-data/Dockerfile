FROM nginx/unit:1.19.0-python3.7
ARG APP_NAME
ARG APP_PORT
WORKDIR /code
COPY requirements.txt /config/requirements.txt
COPY generate_secret_key.py /

RUN apt-get update -y&&\
    apt-get upgrade -y&&\
    # get repo
    apt-get install -y software-properties-common apt-file &&\
    apt-file update && apt-file search add-apt-repository &&\
    # get depencies
    apt-get install -y software-properties-common apt-file libnss3-dev \
    python3-pip python3-dev default-libmysqlclient-dev build-essential\
    mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 sudo\
    git make curl xz-utils file unzip wget&&\
    \
    python3 -m pip install --upgrade pip &&\
    python3 -m pip install --upgrade setuptools &&\
    rm -rf /var/lib/apt/lists/* &&\
    sed -i "$ a alias python=python3" ~/.bashrc &&\
    git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git &&\
    /code/mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y &&\
    pip install -r /config/requirements.txt &&\
    ln -sf /dev/stdout /var/log/unit.log

# Set up for selenium
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && apt-get -y update &&\
    apt-get install -y google-chrome-stable &&\
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
COPY . /code/

# Add init.sh script to docker-entrypoint.sh
RUN sed -i "2i sed -i 's/\r//' /init-scripts/init.sh" /usr/local/bin/docker-entrypoint.sh &&\
    sed -i "3i chmod 700 /init-scripts/init.sh" /usr/local/bin/docker-entrypoint.sh &&\
    sed -i "4i /init-scripts/init.sh $APP_NAME $APP_PORT" /usr/local/bin/docker-entrypoint.sh
