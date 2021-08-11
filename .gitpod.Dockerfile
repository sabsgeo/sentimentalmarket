FROM gitpod/workspace-full:latest

# Install postgres
USER root

RUN P=$(mktemp -d -t) && \
    wget -P $P https://github.com/sabsgeo/sentimentalmarket/raw/main/deps/ta-lib-0.4.0-src.tar.gz && \
    cd $P && tar -xzf ta-lib-0.4.0-src.tar.gz && cd ta-lib/ && ./configure --prefix=/usr && make && make install && \
    rm -rf $P
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

USER root