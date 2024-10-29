import asyncio
import websockets
from playlist import Playlist
from typing import Any
import json
import ast
from ssh import SSHClient
import configparser


config = configparser.ConfigParser()
config.read("settings.ini")

ssh_client = SSHClient(host=config['Cluster']['host'], 
                       port=int(config['Cluster']['port']), 
                       username=config['Cluster']['login'], 
                       password=config['Cluster']['password'])

CLIENTS = set()

playlist = Playlist(pathToDir=config['Music']['music_path'])


def generator_playlist():
    for song in playlist.listSongs:
        for bytes in song.byteArray:
            yield {'artistSong': song.artist + ' - ' + song.name,
                   'bytes': bytes}


musicParts = generator_playlist()


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
        partSong = next(musicParts)
        # print(len(message))

        # data = {
        #     "bytes" : partSong.byteArray[0]
        # }
        # await broadcast(json.dumps({'name': message.name, 'bytes': message.byteArray}))
        # await broadcast(json.dumps({'bytes': ast.literal_eval(message.byteArray[0])}))
        await broadcast(
            json.dumps(ast.literal_eval(str(partSong)))
            )


async def main():
    async with websockets.serve(handler,
                                config['Server']['ip'],
                                int(config['Server']['port'])):
        await broadcast_messages()  # runs forever


if __name__ == "__main__":
    print('run ssh')

    ssh_client.loadArtistInfo(config['Music']['music_path'])
    print('execute script')

    ssh_client.execute(f'./runHugiss.sh {config["Cluster"]["Login"]}')

    ssh_client.fileTransfer('GET', 'artists_summary.json')

    summaryList = json.load(open('artists_summary.json'))

    playlist.readSongInfo(summaryList)

    print('Server Start')
    asyncio.run(main())
