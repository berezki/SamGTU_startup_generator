from cgitb import text
from email.message import Message
from re import I
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters
from telegram import InlineKeyboardMarkup, ReplyMarkup
from telegram import InlineKeyboardButton
from SamgtuBot import SamgtuBot
import sys
import os
import sqlite3
import logging
from pprint import pprint
logging.basicConfig(level=logging.INFO)
from markups import Markups
from random import choice
import commandHandlers
import sys


class TG():
    dispatcher = None
    updater = None


    def create_buttons():
        TG.updater = Updater(sys.argv[1], use_context=True)
        TG.dispatcher = TG.updater.dispatcher
        logging.info('buttons are created')


    def Button(update, context):
        query = update.callback_query
        query.answer()
        match query.data:
            case 'like': # Like
                commandHandlers.like(update)

            case 'generate': # generate startup
                commandHandlers.generate_startup(update)

            case 'default': # default dataset is chosen
                commandHandlers.choose_default_ds(update)

            case 'recuria': # recuria dataset is chosen
                commandHandlers.choose_recuria_ds(update)
            
            case 'changeds': # change dataset
                query.edit_message_text(text="Выберите датасет:", reply_markup=Markups.datasetChooseMarkup)
           
            case 'more': # recuria more
                commandHandlers.recuria_show_more_information(update)
            
            case 'databases':
                commandHandlers.show_list_of_databases(update)

            case '<<<':
                commandHandlers.change_page(update, '-')

            case '>>>':
                commandHandlers.change_page(update, '+')

            case 'newdataset':
                commandHandlers.add_new_dataset(update)
            
            case 'insert':
                connection = sqlite3.connect('GENERATOR.db')
                cursor = connection.cursor()
                cursor.execute('''UPDATE users SET anchor = 1 WHERE id = ?;''', (update.effective_chat.id,))
                connection.commit()
                connection.close()
                context.bot.sendMessage(chat_id=update.effective_chat.id, text='Insert query:')

            case _:
                connection = sqlite3.connect('GENERATOR.db')
                cursor = connection.cursor()
                page = cursor.execute('''SELECT page FROM users WHERE id=?''', (update.effective_chat.id,)).fetchall()[0][0]
                print(query.data[5:])
                lines = cursor.execute(f'SELECT * FROM {query.data[5:]} LIMIT ?,5;', (page*5,)).fetchall()
                connection.close()
                result = query.data.split()[1] + '\n'
                for line in lines:
                    print(line)
                    result += str(line) + '\n'
                context.bot.sendMessage(chat_id=update.effective_chat.id, text=result, reply_markup=Markups.pagesMarkup)


    def start(update, context):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Для начала выберите датасет:", reply_markup=Markups.datasetChooseMarkup)
        connection = sqlite3.connect('GENERATOR.db')
        cursor = connection.cursor()
        cursor.execute('''INSERT OR IGNORE INTO users (id, dataset_id) VALUES (?, ?);''', (update.effective_chat.id, 0))
        connection.commit()
        connection.close()
    
    
    def admin(update, context):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="What u'd like to do?", reply_markup=Markups.adminMarkup)


    def add_handlers():
        TG.dispatcher.add_handler(CommandHandler('start', TG.start))
        TG.dispatcher.add_handler(CommandHandler('admin', TG.admin))
        TG.dispatcher.add_handler(MessageHandler(Filters.text, commandHandlers.get_custom_input, run_async=True))
        TG.dispatcher.add_handler(CallbackQueryHandler(TG.Button))

        logging.info('handlers are added')
    

    def start_bot():
        TG.create_buttons()
        TG.add_handlers()
        TG.updater.start_polling()
        logging.info('bot is started')