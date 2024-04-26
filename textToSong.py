import os
import torch
import torchaudio
from pydub import AudioSegment

class TextToSong:
    def __init__(self) -> None:
        self.device = torch.device('cpu')
        torch.set_num_threads(4)
        self.localModelFile = 'voiceModel.pt'
        self.sample_rate = 48000
        self.speaker = 'aidar'

        if not os.path.isfile(self.localModelFile):
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/ru/ru_v3.pt',
                                        self.localModelFile)  

        self.model = torch.package.PackageImporter(self.localModelFile).load_pickle("tts_models", "model")
        self.model.to(self.device)


    def textToSong(self, text: str) -> None:
        audio_paths = self.model.save_wav(text=text,
                                    speaker=self.speaker,
                                    sample_rate=self.sample_rate,
                                    put_accent=True,
                                    put_yo=True)
        
        # audio = self.model.apply_tts(text=text,
        #                 speaker=self.speaker,
        #                 sample_rate=self.sample_rate)

        self.convertToMP3()

    def convertToMP3(self) -> None:
        AudioSegment.from_wav(os.path.join(os.getcwd(), 'test.wav')).\
            export(os.path.join(os.getcwd(), 'speech_file.mp3'), format="mp3")
