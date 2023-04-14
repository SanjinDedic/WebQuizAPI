import json

from difflib import SequenceMatcher

def similar(s1, s2, threshold=0.6):
    similarity_ratio = SequenceMatcher(None, s1, s2).ratio()
    return similarity_ratio >= threshold

# Example usage:
s1 = "Hello, world!"
s2 = "Hello, everyone!"

print(similar('Orsssn Scott Card', 'Orson Scott Card', 0.6))



def validate_question(json_string):
    try:
        data = json.loads(json_string)
    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return False

    for question in data:
        if not all(key in question for key in ["id", "type", "question", "answer", "image_link"]):
            print("One or more questions are missing required keys.")
            return False

        if question["type"] not in ["multiple_choice", "short_answer"]:
            print("Invalid question type.")
            return False

        if question["type"] == "multiple_choice":
            if "options" not in question or not isinstance(question["options"], list) or len(question["options"]) == 0:
                print("Multiple choice questions must have a non-empty options list.")
                return False

            if not isinstance(question["answer"], str) or len(question["answer"]) != 1 or question["answer"].lower() not in "abcd":
                print("Multiple choice questions must have a valid answer (a, b, c, or d).")
                return False

    return True