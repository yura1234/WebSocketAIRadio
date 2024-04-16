import requests
import json
import ast
from bs4 import BeautifulSoup as bs
# from deep_translator import GoogleTranslator

class Summary:
    
    
    def __init__(self, artistName: str) -> None:
        self.summaryURL = 'https://api.aicloud.sbercloud.ru/public/v2/summarizator/predict'
        self.searchURL = f'https://www.last.fm/ru/music/{artistName}/+wiki'


    def loadDescription(self) -> str:
        page = bs(requests.get(self.searchURL).text)

        if 'У нас пока нет вики-статьи об этом исполнителе' not in page.text:
            return self.__makeQuotes(page.find("div", class_="wiki-content").text[:1000])

        return ''


    def __makeQuotes(self, text: str) -> str:
        return '\"' + text + '\"'


    def makeSummary(self) -> str:
        desc = self.loadDescription()

        if not desc:
            return ''

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        data = {
            "instances": [{
                "text" : desc,
                "num_beams": 10,
                "num_return_sequences": 20,
                "length_penalty": 2.0
                }]
        }

        jsonData = json.dumps(ast.literal_eval(str(data)))
        response = requests.post(self.summaryURL, headers=headers, data=str(jsonData)).json()

        if response['comment'] == 'Ok!':
            return response['prediction_best']['bertscore']
        else:
            return ''
