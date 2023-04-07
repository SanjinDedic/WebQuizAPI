from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import json
from typing import Optional

app = FastAPI()

async def custom_allow_origin(request: Request, call_next):
    allow_origin = False
    origin = request.headers.get('origin', None)

    if origin:
        if '.github.io' in origin or origin.endswith('.repl.co') or origin.startswith('https://replit.com'):
            allow_origin = True

    if allow_origin:
        response = await call_next(request)
    else:
        response = Response(content="CORS not allowed", status_code=400)

    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware('http')(custom_allow_origin)


class SignUp(BaseModel):
    name: str
    password: str
    color: Optional[str] = None
    connected: Optional[int] = None

class Answer(BaseModel):
    id: str
    answer: str
    team_name: str

class Login(BaseModel):
    name: str
    password: str

@app.get("/test")
async def test(request: Request):
      return {"message":"This is a test"}

@app.get("/")
async def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    questions = c.fetchall()
    return {"length": len(questions)}


@app.post("/login")
async def login(team: Login):
    team_name = team.name
    team_password = team.password
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE name = ? AND password = ?", (team_name, team_password))
    team = c.fetchone()
    if team == None:
        return {"message": "Login failed"}
    else:
        return {"message": "Login successful", "score": team[2], "solved_questions": team[3], "color": team[4],"connected": team[5]}


@app.get("/get_question/{id}")
async def get_question(id: str):
    attachment = ''
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE id = ?", (id,))
    question = c.fetchone()
    #print(question)
    if question == None:
        return {"message": "Question not found"}
    else:
        if question[4] != '':
            attachment = '\n' + 'Download starter code ' + question[4] + '\n'
        if question[5] != '':
            attachment += 'Download input file ' + question[5]
        return {"question": question[1] + attachment}
    

@app.get("/download_starter_code/{id}",response_class=FileResponse)
async def download_starter_code(id: str):
    return 'questions/' + id + '_starter.py'


#See if we can download the file from database?
#See if we can attach headers to this response that contain the file name
@app.get("/download_input_file/{id}", response_class=FileResponse)
async def download_input_file(id: str):
    return 'questions/' + id + '_input.txt'


@app.get("/get_teams_table")
async def get_teams_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM teams")
    teams = c.fetchall()
    conn.close()
    return {"teams": teams}


#just need to figure out how to get the solved questions list updated in the database
@app.post("/submit_answer")
async def submit_answer(a: Answer):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE id = ?", (a.id,))
    question = c.fetchone()
    if question == None:
        return {"message": "Question not found"}   
    elif question[1] == a.answer:
        pts = question[2]
        #update the Teams database for the team that solved the question
        #add pts to the score for the team and increment the solved questions
        c.execute("SELECT * FROM teams WHERE name = ?", (a.team_name,))
        team = c.fetchone()
        solved_questions = team[3]
        solved_questions += 1
        score = team[2]
        score += pts
        c.execute("UPDATE teams SET score = ?, solved_questions = ? WHERE name = ?", (score, solved_questions, a.team_name))
        conn.commit()
        return {"message": "Correct"}
    else:
        return {"message": "Incorrect"}

@app.post("/signup")
async def signup(team: SignUp):
    team_name = team.name
    team_password = team.password
    team_color = team.color
    team_connected = team.connected

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if the team already exists
    c.execute("SELECT * FROM teams WHERE name = ?", (team_name,))
    existing_team = c.fetchone()

    if existing_team is not None:
        return {"message": "Team already exists"}

    # Create a new team
    c.execute("INSERT INTO teams (name, password, score, solved_questions, color, connected) VALUES (?, ?, 0, ?, ?, ?)",
              (team_name, team_password, json.dumps([]), team_color, team_connected))
    conn.commit()

    return {"message": "Team created successfully"}

@app.post("/signup")
async def signup(team: SignUp):
    team_name = team.name
    team_password = team.password
    team_color = team.color
    team_connected = team.connected

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if the team already exists
    c.execute("SELECT * FROM teams WHERE name = ?", (team_name,))
    existing_team = c.fetchone()

    if existing_team is not None:
        return {"message": "Team already exists"}

    # Create a new team
    c.execute("INSERT INTO teams (name, password, score, solved_questions, color, connected) VALUES (?, ?, 0, ?, ?, ?)",
              (team_name, team_password, json.dumps([]), team_color, team_connected))
    conn.commit()

    return {"message": "Team created successfully"}
