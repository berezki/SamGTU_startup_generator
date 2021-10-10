from json import load
from random import choice
from typing import Optional
from pydantic import BaseModel
import logging
import sys

class Data(BaseModel):
    token: Optional[str]
    first: list
    second: list


class SamgtuBot:
    data = None

    def loadData():

        with open('data/dataset.json', encoding='utf-8') as ds:
            data_dict = load(ds)
            SamgtuBot.data = Data(**data_dict)
        SamgtuBot.data.token = sys.argv[1]
        
        logging.info('data is loaded ')

        
    def generateIdea() -> str:
        return f'{choice(SamgtuBot.data.first)} {choice(SamgtuBot.data.second)}'
