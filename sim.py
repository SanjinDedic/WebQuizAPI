import sqlite3
import random
import time


#select at random one team from the teams table and give them a random choice of 10, 20 or 30 points

for i in range(10): 
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name FROM teams")
    teams = c.fetchall()
    team = random.choice(teams)[0]
    solved_qs = team[3]
    points = random.choice([10,20,30])
    c.execute("UPDATE teams SET score = score + ?, solved_questions = solved_questions + 1 WHERE name = ?", (points, team))
    print(team, 'scored', points,'points')
    conn.commit()
    time.sleep(8)
    conn.close()
