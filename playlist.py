from base64 import b64encode
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import os
import io
from song import Song
from summary import Summary
from pydub import AudioSegment
from pydub.utils import mediainfo
from pydub.utils import make_chunks
from textToSong import TextToSong
import asyncio
from typing import Awaitable, Any, Callable


class Playlist:


    def __init__(self, pathToDir: str, bitrate: int = 0) -> None:
        self.path = pathToDir

        if self.path[-1] != '\\':
            self.path += '\\'

        if bitrate:
            self.pathToLow = self.path[:self.path.rfind('\\')] + '\\' + f'{bitrate}K'
        else:
            self.pathToLow = str()

        self.bitrate = bitrate
        self.listFiles = self.__readFilesFromDir()
        self.listSongs = list[str]
    

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
    

    def __background(f):
        def wrapped(*args: tuple, **kwargs: dict[str, dict[str, Any]]) -> Awaitable:
            return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

        return wrapped
    

    @__background
    def __convertAudioFile(self, path: str, file: str) -> None:
        newPath = path + '\\' + file

        if os.path.isfile(newPath):
            print(f'{file} file exist. Skip...')
            return
        
        print(f'Convert {file}')
        loadFile = AudioSegment.from_file(self.path + '\\' + file, "mp3")
        loadFile.export(newPath, format="mp3", bitrate=f'{self.bitrate}K')

    
    def __makeDirLowBitFiles(self) -> None:
        listFiles = list(filter(lambda f: f.endswith('mp3') , os.listdir(self.path)))

        if not self.pathToLow:
            return

        if not os.path.isdir(self.pathToLow):
            print(f'Create {self.bitrate}K folder.')
            os.mkdir(self.pathToLow)

        print(f'Need to convert {len(listFiles)} files.')

        loop = asyncio.get_event_loop()
        looper = asyncio.gather(*[self.__convertAudioFile(self.pathToLow, f) for f in listFiles]) 
        loop.run_until_complete(looper)


    def readSongInfo(self) -> None:
        self.__makeDirLowBitFiles()

        for songFilePath in self.listFiles[:2]:
            fullPath = os.path.join(self.path, songFilePath)

            song = MP3(fullPath)
            id3info = ID3(fullPath)

            if self.bitrate:
                audioFile = AudioSegment.from_file(self.pathToLow + '\\' + songFilePath, "mp3")
            else:
                audioFile = AudioSegment.from_file(fullPath, "mp3")

            
            # currentBitrate = mediainfo(self.pathToLow + '\\' + songFilePath)["bit_rate"]
            # lowBitFile = fullPath[:len(fullPath) - 4] + "192k.mp3"

            # audioFile.export(lowBitFile, format="mp3", bitrate="192k")

            chunkMs = 5000
            chunksArray = make_chunks(audioFile, chunkMs)

            songLength = self.__audioDuration(song.info.length)

            summary = Summary(id3info["TPE1"].text[0]).makeSummary()

            if summary == '':
                continue

            makeVoice = TextToSong()
            makeVoice.textToSong(summary)

            # summaryWavPath = os.path.join(os.getcwd(), 'test.wav')
            # audioWavFile = AudioSegment.from_file(summaryWavPath, "wav")
            # chunksWavArray = make_chunks(audioWavFile, chunkMs)

            summaryWavPath = os.path.join(os.getcwd(), 'speech_file.mp3')
            audioWavFile = AudioSegment.from_file(summaryWavPath, "mp3")
            chunksWavArray = make_chunks(audioWavFile, chunkMs)
            
            listBytes = self.__makeBytesFromChunks(chunksWavArray)
            # audioWavFile.export(buff, 'mp3')
            
            # for chunk in chunksWavArray:
            #     buff = io.BytesIO()
            #     chunk.export(buff, 'mp3')
            #     listBytes.append(buff.getvalue())

            self.listSongs.append(Song(
                    name = 'About Artist',
                    artist = '',
                    year = 0,
                    style = '',
                    duration = self.__audioDuration(audioWavFile.duration_seconds),
                    summary = '',
                    byteArray = listBytes
            ))

            if ',' not in id3info["TPE1"].text[0]:
                self.listSongs.append(Song(
                    artist = id3info["TPE1"].text[0],
                    name = id3info["TIT2"].text[0],
                    year = id3info["TDRC"].text[0],
                    style = id3info["TCON"].text[0],
                    duration = songLength,
                    summary = summary,
                    byteArray = self.__makeBytesFromChunks(chunksArray)
                ))

            # print(id3info["TDRC"].text[0]) #Year
            # print(id3info["TCON"].text[0]) #Genre
            # print(id3info["TPE1"].text[0]) #Artist
            # print(id3info["TIT2"].text[0]) #Track
            # print(id3info["APIC"].text[0]) #Image

        # print(*self.listSongs, sep='\n')
