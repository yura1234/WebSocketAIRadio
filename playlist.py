from base64 import b64encode
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import os
import io
from song import Song
from pydub import AudioSegment
# from pydub.utils import mediainfo
from pydub.utils import make_chunks
from textToSong import TextToSong


class Playlist:


    def __init__(self, pathToDir: str) -> None:
        self.path = pathToDir

        if self.path[-1] != '\\':
            self.path += '\\'

        self.listFiles = self.__readFilesFromDir()
        self.listSongs = list()


    def __readFilesFromDir(self) -> list[str]:
        return [f for f in os.listdir(self.path) if f.endswith('.mp3')]


    def __audioDuration(self, length: int) -> tuple[int, int, int]:
        hours = length // 3600  # часы
        length %= 3600
        mins = length // 60  # минуты
        length %= 60
        seconds = length  # секунды

        return int(hours), int(mins), seconds


    def __makeBytesFromChunks(self, chunks: list) -> list[str]:
        listBytes = list()

        for chunk in chunks:
            buff = io.BytesIO()
            chunk.export(buff, 'mp3')
            listBytes.append(str(b64encode(buff.getvalue()))[2:-1])

        return listBytes


    def readSongInfo(self, summaryList: dict[str, str]) -> None:
        audioTags = ['TPE1', 'TIT2']

        for songFilePath in self.listFiles:
            fullPath = os.path.join(self.path, songFilePath)

            song = MP3(fullPath)
            id3info = ID3(fullPath)
            trackTags = id3info.keys()
            artistName = ''
            trackName = ''

            if audioTags[0] in trackTags:
                artistName = id3info["TPE1"].text[0]
            else:
                continue

            if audioTags[1] in trackTags:
                trackName = id3info["TIT2"].text[0]

            summary = ''

            if summaryList[artistName]:
                summary = summaryList[artistName]

            audioFile = AudioSegment.from_file(fullPath, "mp3")

            chunkMs = 5000
            chunksArray = make_chunks(audioFile, chunkMs)

            songLength = self.__audioDuration(song.info.length)

            if summary != '':
                makeVoice = TextToSong()
                makeVoice.textToSong(summary)

                summaryWavPath = os.path.join(os.getcwd(), 'speech_file.mp3')
                audioWavFile = AudioSegment.from_file(summaryWavPath, "mp3")
                chunksAboutArray = make_chunks(audioWavFile, chunkMs)

                listBytes = self.__makeBytesFromChunks(chunksAboutArray)
                self.listSongs.append(Song(
                        name = 'About Artist',
                        artist = '',
                        year = 0,
                        style = '',
                        duration = self.__audioDuration(audioWavFile.duration_seconds),
                        summary = '',
                        byteArray = listBytes
                ))

            # if ',' not in id3info["TPE1"].text[0]:
            self.listSongs.append(Song(
                artist = artistName,
                name = trackName,
                # year = id3info["TDRC"].text[0],
                # name = id3info["TIT2"].text[0],
                # year = id3info["TDRC"].text[0],
                # style = id3info["TCON"].text[0],
                year = 0,
                style = '',
                duration = songLength,
                summary = summary,
                byteArray = self.__makeBytesFromChunks(chunksArray)
            ))

            # print(id3info["TDRC"].text[0]) #Year
            # print(id3info["TCON"].text[0]) #Genre
            # print(id3info["TPE1"].text[0]) #Artist
            # print(id3info["TIT2"].text[0]) #Track
            # print(id3info["APIC"].text[0]) #Image
