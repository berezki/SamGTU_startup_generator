from json import load
from random import choice
import telegram


def loadConfig():
    global config
    with open('data/config.json', encoding='utf-8') as cfg:
        config = load(cfg)


def loadDataSet():
    global first, second
    with open('data/dataset.json', encoding='utf-8') as ds:
        dataset = load(ds)
    first, second = dataset['what'], dataset['with']

    
def generateIdea() -> str:
    return f'{choice(first)} {choice(second)}'


if __name__ == '__main__':
    loadConfig()
    loadDataSet()

    telegram.Bot(token=config['token'])