#!/bin/bash
TAG=0.0.1 
docker run -e SENTRY_URL_CTB=$SENTRY_URL_CTB -it sabugeorgemec/trading-bot:${TAG}
