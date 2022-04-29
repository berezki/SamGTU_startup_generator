import sqlite3
from markups import Markups
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton

def like(update):
    connection = sqlite3.connect('GENERATOR.db')
    cursor = connection.cursor()
    dataset_id = cursor.execute('''SELECT dataset_id FROM users WHERE id = ?;''', (update.effective_chat.id,)).fetchall()[0][0]
    connection.close()
    
    if dataset_id == 0:
        first  = cursor.execute('''SELECT text FROM defaultds WHERE position=1;''').fetchall()
        second = cursor.execute('''SELECT text FROM defaultds WHERE position=2;''').fetchall()
        for first_str in first:
            if update.callback_query.message.text.startswith(first_str):
                cursor.execute('''UPDATE defaultds SET likes = likes + 1 WHERE text = ?;''', (first_str))
                break
        for second_str in second:
            if update.callback_query.message.text.endswith(second_str):
                cursor.execute('''UPDATE defaultds SET likes = likes + 1 WHERE text = ?;''', (second_str))
                break
        connection.commit()
        connection.close()

def generate_startup(update):
    connection = sqlite3.connect('GENERATOR.db')
    cursor = connection.cursor()
    dataset_id = cursor.execute('''SELECT dataset_id FROM users WHERE id = ?''', (update.effective_chat.id,)).fetchall()[0][0]
    match dataset_id:
        case 0:
            first  = cursor.execute('''SELECT text FROM defaultds
                                        WHERE position=1
                                        ORDER BY RANDOM() LIMIT 1''').fetchall()[0][0]
            second = cursor.execute('''SELECT text FROM defaultds
                                        WHERE position=2
                                        ORDER BY RANDOM() LIMIT 1''').fetchall()[0][0]
            result = f'{first} {second}'
            markup = Markups.defaultRegenerateMarkup
        case 1:
            pitch = cursor.execute('''SELECT pitch FROM recuria ORDER BY RANDOM() LIMIT 1''').fetchall()[0][0]
            result = pitch
            markup = Markups.recuriaRegenerateMarkup
    connection.close()
    update.callback_query.edit_message_text(text=result, reply_markup=markup)

def choose_default_ds(update):
    update.callback_query.edit_message_text(text="Успешно выбрано", reply_markup=Markups.generateMarkup)
    connection = sqlite3.connect('GENERATOR.db')
    cursor = connection.cursor()
    cursor.execute('''UPDATE users SET dataset_id = 0 WHERE id = ?;''', (update.effective_chat.id,))
    connection.commit()
    connection.close()

def choose_recuria_ds(update):
    update.callback_query.edit_message_text(text="Успешно выбрано", reply_markup=Markups.generateMarkup)
    connection = sqlite3.connect('GENERATOR.db')
    cursor = connection.cursor()
    cursor.execute('''UPDATE users SET dataset_id = 1 WHERE id = ?;''', (update.effective_chat.id,))
    connection.commit()
    connection.close()

def recuria_show_more_information(update):
    connection = sqlite3.connect('GENERATOR.db')
    cursor = connection.cursor()
    data = cursor.execute('''SELECT name, description FROM recuria WHERE pitch = ?''', (update.callback_query.message.text + '\n',)).fetchall()[0]
    update.callback_query.edit_message_text(text=f'{data[0]} {data[1]}', reply_markup=Markups.recuriaRegenerateMarkup)
    connection.close()

def show_list_of_databases(update):
    db_buttons_list = []
    connection = sqlite3.connect('GENERATOR.db')
    cursor = connection.cursor()
    for table in cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''').fetchall():
        db_buttons_list.append([InlineKeyboardButton(text='table ' + table[0], callback_data='table ' + table[0])])
    connection.close()
    db_markup = InlineKeyboardMarkup(inline_keyboard=db_buttons_list)
    update.callback_query.edit_message_text(text="Choose database", reply_markup=db_markup)

def change_page(update, direction: str):
    table = update.callback_query.message.text.split()[0]
    result = table + '\n'
    connection = sqlite3.connect('GENERATOR.db')
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET page = page {direction} 1 WHERE id = ?;', (update.effective_chat.id,))
    connection.commit()
    page = cursor.execute('''SELECT page FROM users WHERE id=?''', (update.effective_chat.id,)).fetchall()[0][0]
    lines = cursor.execute(f'SELECT * FROM {table} LIMIT ?,5;', (page*5,)).fetchall()
    connection.close()
    for line in lines:
        result += str(line) + '\n'
    update.callback_query.edit_message_text(text=result, reply_markup=Markups.pagesMarkup)

def add_new_dataset(update):
    # https://docs.google.com/spreadsheets/d/1MNI9BDxlrKdaol4BJLI17Eb6N1ErcED-0inp4fwE_1U/edit?usp=sharing
    update.callback_query.edit_message_text(text='Please send link to google')
    connection = sqlite3.connect('GENERATOR.db')
    cursor = connection.cursor()
    cursor.execute('''UPDATE users SET anchor = 0 WHERE id = ?;''', (update.effective_chat.id,))
    connection.commit()
    connection.close()

def get_custom_input(update, context):
    connection = sqlite3.connect('GENERATOR.db')
    cursor = connection.cursor()
    anchor = cursor.execute('''SELECT anchor FROM users WHERE id = ?;''', (update.effective_chat.id,)).fetchall()[0][0]
    match anchor:
        case 0:
            cursor.execute('''INSERT INTO customds (host_id, link) VALUES (?, ?);''', (update.effective_chat.id, update.message.text))
            cursor.execute('''UPDATE users SET anchor = 3 WHERE id = ?;''', (update.effective_chat.id,))
            context.bot.sendMessage(chat_id=update.effective_chat.id, text='What is the name of dataset?')
        case 3:
            cursor.execute('''UPDATE customds SET name = ? WHERE id = ?;''', (update.message.text, update.effective_chat.id))
            cursor.execute('''UPDATE users SET anchor = -1 WHERE id = ?;''', (update.effective_chat.id,))
            context.bot.sendMessage(chat_id=update.effective_chat.id, text='Dataset added')
        case 1:
            cursor.execute('''UPDATE users SET anchor = -1 WHERE id = ?;''', (update.effective_chat.id,))
            context.bot.sendMessage(chat_id=update.effective_chat.id, text=cursor.execute(update.message.text).fetchall())
    connection.commit()
    connection.close()