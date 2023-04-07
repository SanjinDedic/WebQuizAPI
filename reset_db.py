import os, sqlite3
import json

#create a list of questions based on the questions folder
import sqlite3
import os

os.remove('database.db')
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE questions
                (id text, answer text, points integer)''')

#add the questions to the database by reading the questions.json file
with open('questions.json') as f:
    questions = json.load(f)

for q in questions:
    print(q)
    print(q['id'], q['answer'], q['points'])
    c.execute("INSERT INTO questions VALUES (?, ?, ?)", (q['id'], q['answer'], q['points']))




c.execute('''CREATE TABLE teams
                (name text, password text, score integer, solved_questions integer, color text, connected boolean)''')

c.execute('''CREATE TABLE grokkers
                (name text, password text, score integer, solved_questions integer, color text, connected boolean)''')



#add the teams to the database

c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)", ('Mount Waverley', 'abc', 0, 0, '#EAB676', False))
c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)", ('Box Hill', 'abc', 0, 0, '#00AD50', False))
c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)", ('Melbourne High', 'abc', 0, 0, '#2595BE', False))
c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)", ('Wantirna', 'abc', 0, 0, '#AD00A2', False))

conn.commit()
conn.close()

print('Database created successfully')
