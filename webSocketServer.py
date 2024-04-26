import asyncio
import websockets
import pickle
from playlist import Playlist
from typing import Any
import json
import ast

CLIENTS = set()
ip = 'localhost'
port = 5000

# with open('playlist.pickle', 'rb') as f:
#     playlist = pickle.load(f)

# playlist = Playlist('D:\\Music\\Various Artists - Retrospective View 3 (2019)', 0)
playlist = Playlist('C:\\Users\\Yura\\Documents\\pyProjects\\music')

def generator_test():
    for song in playlist.listSongs:
        yield song
        # for bytes in song.byteArray:
        #     yield bytes

music_gen = generator_test()

# arr = iter(range(1, 100))

async def handler(websocket):
    CLIENTS.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        CLIENTS.remove(websocket)

async def send(websocket, message):
    try:
        await websocket.send(message)
    except websockets.ConnectionClosed:
        pass

async def broadcast(message):
    for websocket in CLIENTS:
        asyncio.create_task(send(websocket, message))

async def broadcast_messages(): 
    while True:
        print(f"Clients = {len(CLIENTS)}")

        await asyncio.sleep(3)
        message = next(music_gen)
        # print(len(message))

        data = {
            "bytes" : message.byteArray[0]
        }
        # await broadcast(json.dumps({'name': message.name, 'bytes': message.byteArray}))
        # await broadcast(json.dumps({'bytes': ast.literal_eval(message.byteArray[0])}))
        await broadcast(
            json.dumps(ast.literal_eval(str(data)))
            )

async def main():
    async with websockets.serve(handler, ip, port):
        await broadcast_messages()  # runs forever

if __name__ == "__main__":
    playlist.readSongInfo()
    # message = next(music_gen)

    # print(len(message))
    # print(len(gzip.compress(bytes(message, 'utf-8'))))
    print('Server Start')
    asyncio.run(main())
