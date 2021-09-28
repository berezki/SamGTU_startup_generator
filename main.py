from json import load
from random import choice
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton


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

    updater = Updater(token=config['token'], use_context=True)
    dispatcher = updater.dispatcher

    regenerateButton = InlineKeyboardButton(text='Regenerate', callback_data='1')
    regenerateMarkup = InlineKeyboardMarkup(inline_keyboard=[[regenerateButton]])

    def button(update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=generateIdea(), reply_markup=regenerateMarkup)
    def start(update, context):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Use /startup to generate")
    def startup(update, context):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=generateIdea(), reply_markup=regenerateMarkup)
    
    start_handler = CommandHandler('start', start)
    startup_handler = CommandHandler('startup', startup)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(startup_handler)
    dispatcher.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()