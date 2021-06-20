#!/bin/bash
P=$(mktemp -d -t)
wget -P $P https://github.com/sabsgeo/crypto-trading-bot/raw/main/deps/ta-lib-0.4.0-src.tar.gz
cd $P && tar -xzf ta-lib-0.4.0-src.tar.gz && cd ta-lib/ && ./configure --prefix=/usr && make && sudo make install
# clean up
rm -rf $P
