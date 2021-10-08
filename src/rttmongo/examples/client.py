import json
import asyncio
import websockets


async def main():

    uri = "ws://0.0.0.0:8000/users"

    try:
        async with websockets.connect(uri) as websocket:
            print('listening on')
            while True:
                await asyncio.sleep(2)

                data = await websocket.recv()
                print('received change: ', json.loads(data))
    except (Exception,) as err:
        print('error: ', err)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())