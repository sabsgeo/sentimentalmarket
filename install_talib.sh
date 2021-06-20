#!/bin/bash
P=$(mktemp -d -t)
wget -P $P https://github.com/sabsgeo/sentimentalmarket/raw/main/deps/ta-lib-0.4.0-src.tar.gz
cd $P && tar -xzf ta-lib-0.4.0-src.tar.gz && cd ta-lib/ && ./configure --prefix=/usr && make && make install
# clean up
rm -rf $P
# export PIP_USER=no was required for development in git pod for installing python package into virtual environment
