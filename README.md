# Crypto Market Notifier
This is a docker application which will send you triggers by checking trading indicators
Right now trading indictor that is been inregrated is RSI.
More indicators will be added soon

## How to run the application
This application is made with docker as the environment management system. So assumption is that
the host system will have docker installed.

Here is the sample command to build the docker
```
TAG=0.0.1 docker build -t sabugeorgemec/trading-bot:${TAG} .
```
## How to run the docker
For this docker to run and send you notification you need a telegram channel id and an API key to communicate with the channel.
Following are the steps to follow to get these two information.
1. Make public telegram channel from the telegram mobile application
2. Make a telegram bot by visting the channel @BotFather and typing /start
3. Save the api key for the telegram bot which will auth the bot to post messaged in channel
4. Make yourself and telegram bot admin of the public telegram channel that you created so that the bot can post the messages
5. Get the channel ID by forwarding a message from the channel to @JsonDumpBot

Now to run the docker use the following sample command
```
TAG=0.0.1 API_KEY=<api-key> CHAN_ID=<channel-id> docker run -it sabugeorgemec/trading-bot:${TAG} eth "${API_KEY}" "${CHAN_ID}"
```

## Rules that are coded
1. If the RSI > 70 or RSI < 30 the channel will notification
2. If the RSI value goes above 70 and when it reaches to the top and then starts to come down it will send notification
3. If the RSI value goes below 30 and when it reaches the bottom and then starts to come up then it will send notification

## Future plan
1. Add MACD indicator and integrate with RSI
2. Add VWAP indicator and integrate to both RSI and MACD
3. Add candle stick patten detection

## Disclamer
I am not a market expert I am just coding things that I have learned from my information sources