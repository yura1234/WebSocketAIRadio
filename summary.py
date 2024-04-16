import requests
import json
import ast
from bs4 import BeautifulSoup as bs
from deep_translator import GoogleTranslator

class Summary:
    
    
    def __init__(self, artistName: str) -> None:
        self.summaryURL = 'https://api.aicloud.sbercloud.ru/public/v2/summarizator/predict'
        self.searchURL = f'https://www.last.fm/ru/music/{artistName}/+wiki'

        self.__findOk = True

        self.__page = bs(requests.get(self.searchURL).text)

        self.tranlatedText = self.__makeQuotes(self.__page.find("div", class_="wiki-content").text[:1000])

        # self.tranlatedText = self.__makeQuotes(self.__page.find("div", class_="wiki-content").text[:100])

        # if 'We don\'t have a wiki for this artist.' not in self.__page.text: 
        #     self.__findOk = True
        #     self.__sourceText = self.__page.find("div", class_="wiki-content").text[:1000]
        #     self.__translator = GoogleTranslator(source='en', target='ru')

        #     self.tranlatedText = self.__makeQuotes(self.__translator.translate(self.__sourceText))
    

    def __makeQuotes(self, text: str) -> str:
        return '\"' + text + '\"'
        # if text[0] != '\"':
        #     text[0] = '\"'
        # if text[len(text) - 1] != '\"':
        #     text[len(text) - 1] = '\"'


    def makeSummary(self) -> str:
        if self.__findOk == False:
            return ''

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "instances": [{
                # "text" : self.tranlatedText[:(int)(len(self.tranlatedText) / 3)] + '\"',
                "text" : self.tranlatedText,
                "num_beams": 10,
                "num_return_sequences": 20,
                "length_penalty": 2.0
                }]
        }

        jsonData = json.dumps(ast.literal_eval(str(data)))
        print(jsonData)
        response = requests.post(self.summaryURL, headers=headers, data=str(jsonData)).json()

        if response['comment'] == 'Ok!':
            return response['prediction_best']['bertscore']
        else:
            return ''
        

if __name__ == '__main__':
    print(Summary('Prodigy').makeSummary())