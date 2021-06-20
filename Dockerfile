FROM debian:buster

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    ca-certificates \
    python3-dev \
    python3-pip \
    git \
    python3-setuptools

RUN wget https://raw.githubusercontent.com/sabsgeo/sentimentalmarket/main/install_talib.sh && \
    chmod +x install_talib.sh && \
    ./install_talib.sh 

RUN python3 -m pip install --upgrade --force-reinstall pip && pip3 install git+https://github.com/sabsgeo/sentimentalmarket.git

COPY example/* /
ENTRYPOINT ["python3", "-u", "/main.py"]


