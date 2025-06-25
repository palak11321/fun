# Import necessary modules
import asyncio
import json
import ssl
import websockets
import requests
from google.protobuf.json_format import MessageToDict
from example import *
import MarketDataFeedV3_pb2 as pb


def get_market_data_feed_authorize_v3():
    """Get authorization for market data feed."""
    access_token = 'eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiJBUDQyNDAiLCJqdGkiOiI2ODVhNTIzNWU5NjQyYzM0ODUwZmRkNGQiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNQbHVzUGxhbiI6dHJ1ZSwiaWF0IjoxNzUwNzQ5NzQ5LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3NTA4MDI0MDB9.Skl7oJM_xpzvY3xYhpV_wnvfJb9tGQLCMaLVEqPsU68'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    url = 'https://api.upstox.com/v3/feed/market-data-feed/authorize'
    api_response = requests.get(url=url, headers=headers)
    return api_response.json()


def decode_protobuf(buffer):
    """Decode protobuf message."""
    feed_response = pb.FeedResponse()
    feed_response.ParseFromString(buffer)
    return feed_response


async def fetch_market_data():
    """Fetch market data using WebSocket and print it."""

    # Create default SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Get market data feed authorization
    response = get_market_data_feed_authorize_v3()
    # Connect to the WebSocket with SSL context
    async with websockets.connect(response["data"]["authorized_redirect_uri"], ssl=ssl_context) as websocket:
        print('Connection established')

        await asyncio.sleep(1)  # Wait for 1 second

        # Data to be sent over the WebSocket
        data = {
            "guid": "someguid",
            "method": "sub",
            "data": {
                "mode": "full",
                # "instrumentKeys": ["NSE_INDEX|Nifty 50"]
                "instrumentKeys": ["NSE_INDEX|Nifty 50", "NSE_FO|71381", "NSE_FO|71382"]#NSE_FO|71382-pe
            }
        }

        # Convert data to binary and send over WebSocket
        binary_data = json.dumps(data).encode('utf-8')
        await websocket.send(binary_data)

        # Continuously receive and decode data from WebSocket
        n = 0
        while True:
            message = await websocket.recv()

            decoded_data = decode_protobuf(message)
            print('Received data:', decoded_data)
            # print("name:", "NSE_INDEX|Nifty 50", end="/n")
            # print("ohlc value", decoded_data.feeds["NSE_INDEX|Nifty 50"].fullFeed.indexFF.marketOHLC.ohlc[1])
            # print('marketOHLC.ohlc[]:', decoded_data.marketOHLC.ohlc)
            data = MessageToDict(decoded_data)
            # Fetch last 1 minute historical candle for Nifty 50
            last_minute_data = get_last_minute_candle("NSE_INDEX|Nifty 50")
            print(n,end='\n\n')
            print('Data as dictionary:', data, end='\n\n\n')
            n += 1
            if n % 10 == 0: # Print every 10th message
                pass

            if "feeds" not in data:
                pass
            else :
                
                # nifty_50 = data['feeds']["NSE_INDEX|Nifty 50"]["fullFeed"]["indexFF"]["marketOHLC"]["ohlc"][1]
                nifty_spot = data['feeds']["NSE_INDEX|Nifty 50"]["fullFeed"]["indexFF"]["marketOHLC"]["ohlc"][1]
                nifty_spot_delay = data['open,']
                nifty_pe = data['feeds']["NSE_FO|71382"]["fullFeed"]["marketFF"]["marketOHLC"]["ohlc"][1]
                nifty_ce = data['feeds']["NSE_FO|71381"]["fullFeed"]["marketFF"]["marketOHLC"]["ohlc"][1]
                # nifty_spot = candle_data_return(nifty_spot)
                # nifty_pe = candle_data_return(nifty_pe)
                # nifty_ce = candle_data_return(nifty_ce)
                # print(f"Nifty Spot: {n
                # ifty_spot}, Nifty PE: {nifty_pe}, Nifty CE: {nifty_ce}")
            previous_candle_data_return()
            # print(previous_candle_data_return())
            # break
            print(f"Nifty aman Open: {nifty_spot['high']}, Nifty PE Open: {nifty_pe}, Nifty CE Open: {nifty_ce}")
            print(f"Nifty Spotttcheckt Open: {nifty_spot.get('open')}, Nifty PE Open: {nifty_pe.get('open')}, Nifty CE Open: {nifty_ce.get('open')}")
            fhg()
            
              # Call the placeholder function from the example module
            # breakpoint()
            # try :
            #     
            # except KeyError as e:
            #     pass
            # nifty_50 = data['feeds']["NSE_INDEX|Nifty 50"]["fullFeed"]["indexFF"]["marketOHLC"]["ohlc"][1]
            # nifty_100 = data_dict['feeds']["NSE_INDEX|Nifty 100"]["fullFeed"]["indexFF"]["marketOHLC"]["ohlc"][1]
            # nifty_bank = data_dict['feeds']["NSE_INDEX|Nifty Bank"]["fullFeed"]["indexFF"]["marketOHLC"]["ohlc"][1]
            # print(f"Nifty 50: {nifty_50}")
            # print(f"Nifty 50: {nifty_50}, Nifty 100: {nifty_100}, Nifty Bank: {nifty_bank}")
            # Convert the decoded data to a dictionary
            # data_dict = MessageToDict(decoded_data)

            # Print the dictionary representation
            # print(json.dumps(data_dict))


# Execute the function to fetch market data
asyncio.run(fetch_market_data())