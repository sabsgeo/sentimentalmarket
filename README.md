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

## Websockets and REST API's used for data access
In the code I have used two modes to gets the data.
1. REST API is used to get the historical data for about 500 data points which is done at the start of the application
2. Websocket for continious addition of data to the above data

Max amount of data that will be used for calculation will be 500 or the max amount of data if the number of data points are less than 500

### REST API
Below is the API that is used for historical data collection in candle stick format
```
https://api.binance.com/api/v3/klines?symbol=<symbol>&interval=<interval>
```
Examples of symbols ETHUSDT, XRPUSDT etc 
Examples for intervals 1m 15m 1h etc
Example data output format
```
[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]
```

### Websocket
Two websockets are used to get real time data 

1. Below is the API that is used for realtime data of candle stick

```
wss://stream.binance.com:9443/ws/<symbol>@kline_<interval>
```
Examples of symbols ethusdt, xrpusdt etc 
Examples for intervals 1m 15m 1h etc
Example data output format

```
{
  "e": "kline",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}
```

2. Below id the API that is used for realtime price

```
'wss://stream.binance.com:9443/ws/<symbols>usdt@trade'
```
Examples of symbols ethusdt, xrpusdt etc 
Example data output format
```
{
  "e": "trade",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "t": 12345,       // Trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "b": 88,          // Buyer order ID
  "a": 50,          // Seller order ID
  "T": 123456785,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore
}
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