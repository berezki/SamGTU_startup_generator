from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from SamgtuBot import SamgtuBot



class TG():
    dispatcher = None
    updater = None
    regenerateButton = None
    regenerateMarkup = None


    def create_buttons():
        TG.updater = Updater(token=SamgtuBot.data.token, use_context=True)
        TG.dispatcher = TG.updater.dispatcher
        TG.regenerateButton = InlineKeyboardButton(text='Regenerate', callback_data='1')
        TG.regenerateMarkup = InlineKeyboardMarkup(inline_keyboard=[[TG.regenerateButton]])

        print('buttons are created')

    def button(update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=SamgtuBot.generateIdea(), reply_markup=TG.regenerateMarkup)
    def start(update, context):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Use /startup to generate")
    def startup(update, context):
        context.bot.sendMessage(chat_id=update.effective_chat.id, text=SamgtuBot.generateIdea(), reply_markup=TG.regenerateMarkup)
    
    def add_handlers():
    
        start_handler = CommandHandler('start', TG.start)
        startup_handler = CommandHandler('startup', TG.startup)

        TG.dispatcher.add_handler(start_handler)
        TG.dispatcher.add_handler(startup_handler)
        TG.dispatcher.add_handler(CallbackQueryHandler(TG.button))

        print('handlers are added')
    
    def start_bot():
        TG.create_buttons()
        TG.add_handlers()
        TG.updater.start_polling()
        print('bot is started')