from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton


class Markups:
    # Buttons:
    likeButton                  = InlineKeyboardButton(text='\U00002665',    callback_data='like')
    generateButton              = InlineKeyboardButton(text='Generate',      callback_data='generate')
    chooseDefaultDatasetButton  = InlineKeyboardButton(text='Default',       callback_data='default')
    chooseRecuriaDatasetButton  = InlineKeyboardButton(text='Recuria',       callback_data='recuria')
    changeDatasetButton         = InlineKeyboardButton(text='Change dataset',callback_data='changeds')
    moreButton                  = InlineKeyboardButton(text='More',          callback_data='more')
    databasesButton             = InlineKeyboardButton(text='Databases',     callback_data='databases')
    insertRequestButton         = InlineKeyboardButton(text='Insert request',callback_data='insert')
    prevButton                  = InlineKeyboardButton(text='<<<',           callback_data='<<<')
    nextButton                  = InlineKeyboardButton(text='>>>',           callback_data='>>>')
    addNewDatasetButton         = InlineKeyboardButton(text='New',           callback_data='newdataset')
    
    # Markups:
    generateMarkup          = InlineKeyboardMarkup(inline_keyboard=[[generateButton]])
    datasetChooseMarkup     = InlineKeyboardMarkup(inline_keyboard=[[chooseDefaultDatasetButton, chooseRecuriaDatasetButton],[addNewDatasetButton]])
    defaultRegenerateMarkup = InlineKeyboardMarkup(inline_keyboard=[[generateButton],[changeDatasetButton, likeButton]])
    recuriaRegenerateMarkup = InlineKeyboardMarkup(inline_keyboard=[[generateButton],[changeDatasetButton, moreButton]])
    adminMarkup             = InlineKeyboardMarkup(inline_keyboard=[[databasesButton]])
    pagesMarkup             = InlineKeyboardMarkup(inline_keyboard=[[insertRequestButton],[prevButton, nextButton]])
