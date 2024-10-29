import paramiko
import json
import os
from mutagen.id3 import ID3
from summary import Summary


class SSHClient():


    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self.userName = username
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=host, username=username, password=password, port=port)


    def execute(self, command: str) -> str:
        _, stdout, stderr = self.client.exec_command(command)
        data = stdout.read() + stderr.read()

        return data.decode()


    def loadArtistInfo(self, path: str) -> None:
        files = [f for f in os.listdir(path) if f.endswith('.mp3')]
        trackSeps = [',', 'feat.', '&', 'и', ';']
        json_data = {}

        for song in files:
            summary = ''
            fullPath = os.path.join(path, song)

            id3info = ID3(fullPath)
            trackTags = id3info.keys()
            artistName = ''

            if 'TPE1' in trackTags:
                artistName = id3info["TPE1"].text[0]
            else:
                continue

            for sep in trackSeps:
                if sep in artistName:
                    artists = artistName.split(sep)
                    for artist in artists:
                        summary += Summary(artist.strip()).loadDescription() + '\n'
                    break

            if summary == '':
                summary = Summary(artistName).loadDescription()
            if summary == '':
                continue

            json_data[artistName] = summary

        with open('artists.json', 'w') as out:
            json.dump(json_data, out)

        self.fileTransfer('POST', 'artists.json')


    def fileTransfer(self, method: str, fileName: str) -> None:
        localPath = os.path.join(os.getcwd(), fileName)
        remotePath = f'/home/{self.userName}/{fileName}'

        with self.client.open_sftp() as sftp:
            if method == 'GET':
                print(f'Transfer from remote {remotePath} to local {localPath}')
                sftp.get(remotePath, localPath)
            elif method == 'POST':
                print(f'Transfer from local {localPath} to remote {remotePath}')
                sftp.put(localPath, remotePath)


    def close(self) -> None:
        self.client.close()
