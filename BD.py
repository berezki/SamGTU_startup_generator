import sqlite3
import json


############# setting up users table #############

connection = sqlite3.connect('GENERATOR.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER UNIQUE,
    page UNSIGNED INTEGER DEFAULT 0,
    anchor INTEGER DEFAULT 0,
    admin INTEGER DEFAUlT 0,
    dataset_id INTEGER
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS customds (
    id INTEGER UNIQUE,
    name TEXT,
    host_id INTEGER,
    link TEXT
);''')

# anchors:
# 0 - enter dataset
# 1 - enter query
# 2 - enter name of database
# 3 - enter name of custom dataset

# dataset ids:
# 0 - default
# 1 - recuria


############# setting up default dataset #############

cursor.execute('''CREATE TABLE IF NOT EXISTS defaultds (
    text TEXT UNIQUE,
    position INTEGER,
    likes INTEGER DEFAULT 0
);''')

with open('data/dataset.json', 'r', encoding='utf-8') as dtst:
    data = json.load(dtst)
    for first_str in data['first']:
        cursor.execute('''INSERT OR IGNORE INTO defaultds (text, position) VALUES (?,?);''', (first_str,1))
    for second_str in data['second']:
        cursor.execute('''INSERT OR IGNORE INTO defaultds (text, position) VALUES (?,?);''', (second_str,2))

############# setting up recuria dataset #############


cursor.execute('''CREATE TABLE IF NOT EXISTS recuria (
                                            name TEXT UNIQUE,
                                            pitch TEXT,
                                            description TEXT,
                                            likes INTEGER DEFAULT 0
);''')

with open('recuria/names.txt', 'r', encoding='utf-8') as nms:
    names = nms.readlines()
with open('recuria/pitches.txt', 'r', encoding='utf-8') as ptchs:
    pitches = ptchs.readlines()
with open('recuria/descriptions.txt', 'r', encoding='utf-8') as dscriptns:
    descriptions = dscriptns.readlines()

for i in range(6091):
    cursor.execute('''INSERT OR IGNORE INTO recuria (name, pitch, description) VALUES (?, ?, ?);''', (names[i], pitches[i], descriptions[i]))

connection.commit()
connection.close()