from json import load
from random import choice
from pydantic import BaseModel 

class Data(BaseModel):
    token: str
    first: list
    second: list


class SamgtuBot:
    data = None

    def loadData():

        with open('data/config.json', encoding='utf-8') as cfg:
            config_dict = load(cfg)
        with open('data/dataset.json', encoding='utf-8') as ds:
            dataset_dict = load(ds)
        data_dict = config_dict | dataset_dict

        SamgtuBot.data = Data(**data_dict)

        print('data is loaded ')

        
    def generateIdea() -> str:
        return f'{choice(SamgtuBot.data.first)} {choice(SamgtuBot.data.second)}'
