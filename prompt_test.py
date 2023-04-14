import openai
import json
from validator import *
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('API_KEY')



def merge_json_strings(json_str1, json_str2):
    json_str1 = json_str1.replace('\n', '').replace('    ', '')
    json_str2 = json_str2.replace('\n', '').replace('    ', '')

    data1 = json.loads(json_str1)
    data2 = json.loads(json_str2)

    if isinstance(data1, list) and isinstance(data2, list):
        merged_data = data1 + data2
    else:
        raise ValueError("Incompatible data types for merging")

    merged_json_string = json.dumps(merged_data, separators=(',', ':'))

    return merged_json_string

def create_4(topic="football"):
    counter = 0
    template = '''
    [
    {
        "id":1,
        "type": "multiple_choice",
        "question": "What is absolute zero temp?",
        "options": ["-273.15","0","-44.5","-99"],
        "answer": "a",
        "image_link": ""
    },
    {
        "id":2,
        "type": "short_answer",
        "question": "What does CPU stand for?",
        "answer": "Central Processing Unit",
        "image_link": ""
    }
    ]
        '''
    prompt = f'''Generate a quiz about {topic} with 4 questions in JSON format using this template:{template} Ensure a valid JSON output use " instead of '. Multiple choice questions should have 4 options. Use only multiple_choice and short_answer types.'''

    # Send the prompt to the GPT-3.5 API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Extract the generated text from the response
    generated_text = response.choices[0].text.strip()

    if validate_question(generated_text):
        return generated_text.replace('\n', '').replace('    ', '')
    else:
        counter += 1
        if counter > 3:
            return {'error': 'too many attempts'}
        else:
            return create_4(topic)

def create_quiz(topic="football", num=4):
    if num > 12:
        num = 12
    else:
        r = num % 4
        num = num - r
    if num == 4:
        ans = create_4(topic)
        return json.loads(ans)
    elif num == 8:
        a = create_4(topic)
        b = create_4(topic)
        ans = merge_json_strings(a, b)
        return json.loads(ans)
    elif num == 12:
        a = create_4(topic)
        b = create_4(topic)
        c = create_4(topic)
        ans = merge_json_strings(c, merge_json_strings(a, b))
        return json.loads(ans)

print(create_quiz("football", 4))

json1 = '''[
  {
    "id":1,
    "type": "multiple_choice",
    "question": "Who is known as the father of computer science?",
    "options": [
      "Charles Babbage",
      "Alan Turing",
      "John von Neumann",
      "Ada Lovelace"
    ],
    "answer": "a",
    "points": 10,
    "image_link": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Charles_Babbage_1860.jpg"
  },
  {
    "id":2,
    "type": "short_answer",
    "question": "What does CPU stand for?",
    "answer": "Central Processing Unit",
    "points": 10,
    "image_link": ""
  },
  {
    "id":3,
    "type": "multiple_choice",
    "question": "Which of the following is the first commercially successful video game?",
    "options": [
      "Tennis for Two",
      "Pong",
      "Space Invaders",
      "Pac-Man"
    ],
    "answer": "b",
    "points": 10,
    "image_link": "https://upload.wikimedia.org/wikipedia/commons/f/f8/Pong.png?20060521134835"
  },
  {
    "id":4,
    "type": "short_answer",
    "question": "What was the name of the first electronic general-purpose computer?",
    "answer": "ENIAC",
    "points": 10,
    "image_link": ""
  },
      {
    "id": 5,
    "type": "multiple_choice",
    "question": "Which programming language was developed by James Gosling at Sun Microsystems?",
    "options": [
      "Python",
      "Java",
      "C++",
      "Ruby"
    ],
    "answer": "b",
    "points": 10,
    "image_link": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Java_Logo.svg/1200px-Java_Logo.svg.png"
  }
  ]'''

json2 = '''[
  {
    "id": 6,
    "type": "short_answer",
    "question": "What does the acronym RAM stand for?",
    "answer": "Random Access Memory",
    "points": 10,
    "image_link": ""
  },
  {
    "id": 7,
    "type": "multiple_choice",
    "question": "Which company was founded by Bill Gates and Paul Allen?",
    "options": [
      "Apple",
      "Microsoft",
      "IBM",
      "Hewlett-Packard"
    ],
    "answer": "b",
    "points": 10,
    "image_link": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Microsoft_logo_%282012%29.svg/1200px-Microsoft_logo_%282012%29.svg.png"
  },
  {
    "id": 8,
    "type": "short_answer",
    "question": "What does the acronym URL stand for?",
    "answer": "Uniform Resource Locator",
    "points": 10,
    "image_link": ""
  },
  {
    "id": 9,
    "type": "multiple_choice",
    "question": "What was the first web browser invented by Sir Tim Berners-Lee?",
    "options": [
      "Mosaic",
      "Netscape Navigator",
      "Internet Explorer",
      "WorldWideWeb"
    ],
    "answer": "d",
    "points": 10,
    "image_link": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Sir_Tim_Berners-Lee_%28cropped%29.jpg/800px-Sir_Tim_Berners-Lee_%28cropped%29.jpg"
  },
  {
    "id": 10,
    "type": "short_answer",
    "question": "What is the name of the scientist who invented the World Wide Web?",
    "answer": "Tim Berners-Lee",
    "points": 10,
    "image_link": ""
  }
]
'''

data = merge_json_strings(json1, json2)
print(data)
