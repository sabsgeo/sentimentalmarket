#!/bin/bash
if [[ "$1" == "sc" ]]
then
cd example && python main.py
else
TAG=0.0.1 
docker run -e SENTRY_URL_CTB=$SENTRY_URL_CTB -it sabugeorgemec/trading-bot:${TAG}
fi 
