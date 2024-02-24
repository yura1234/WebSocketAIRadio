from playlist import Playlist
import io
from pydub import AudioSegment

def main() -> None:
    p = Playlist('D:\\Music\\Various Artists - Retrospective View 3 (2019)')
    p.readSongInfo()
    print(p.listSongs)


    # bytesArray = p.listSongs[0].byteArray

    # sample = io.BytesIO(bytes(bytesArray[0], encoding="utf-8"))
    # sample = io.BytesIO(bytesArray[0])
    # AudioSegment.from_file(sample).export('maga', 'mp3')
    # AudioSegment.from_file(sample).export(, format='mp3')
    # print(bytesArray[0].read().decode('UTF-8'))
    # print(bytesArray[0])
    # test = AudioSegment(bytesArray[0], sample_width=2, frame_rate=44100, channels=2)

    t = 1



if __name__ == '__main__':
    # pass
    main()
    # path = 'C:\\Users\\Yura\\Desktop\\MorozovDA-main\\WindowsFormsAppNext\\bin\\Debug\\netcoreapp3.1'
    # from os import listdir
    # from os.path import isfile, join
    # import uuid

    # def makeTag(fileName: str) -> str:
    #     return f'<Component Id=\"{fileName}\" Guid=\"{uuid.uuid1()}\">\n\t<File Id=\"{fileName}\" Source=\"$(var.sourceFolder){fileName}\"/>\n</Component>'
            

    # onlyfiles = [makeTag(f) for f in listdir(path) if isfile(join(path, f))]
    # print(*onlyfiles, sep='\n')
