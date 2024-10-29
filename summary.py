import requests
from bs4 import BeautifulSoup as bs
import ast
# from deep_translator import GoogleTranslator
import json


class Summary:
    
    
    def __init__(self, artistName: str) -> None:
        artistName = artistName.replace(' ', '%20')
        self.summaryURL = 'https://api.aicloud.sbercloud.ru/public/v2/summarizator/predict'
        self.searchURL = f'https://www.last.fm/ru/music/{artistName}/+wiki'
        self.description = ''


    def loadDescription(self) -> str:
        print(f'GET {self.searchURL}')
        response = requests.get(self.searchURL)

        if response.status_code == 200:
            page = bs(response.text, 'html.parser')

            if 'У нас пока нет вики-статьи об этом исполнителе' not in page.text:
                return self.__makeQuotes(page.find("div", class_="wiki-content").text[:1000])

        return ''


    def __makeQuotes(self, text: str) -> str:
        return '\"' + text + '\"'


    def makeSummary(self) -> str:
        if not self.description:
            self.description = self.loadDescription()

        if not self.description: 
            return ''

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        data = {
            'instances': [{
                'text' : self.description,
                'num_beams': 10,
                'num_return_sequences': 20,
                'length_penalty': 2.0
                }]
        }

        
        data = json.dumps(ast.literal_eval(str(data)))
        print(f'POST {self.summaryURL}')

        response = requests.post(self.summaryURL, headers=headers, data=str(data))

        if response.status_code == 200:
            response = response.json()
            if response['comment'] == 'Ok!':
                return response['prediction_best']['bertscore']
        else:
            return ''
