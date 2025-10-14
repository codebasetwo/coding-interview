import os
import json

from openai import OpenAI
from typing import Dict, Any
from dotenv import load_dotenv

from .prompts import system_prompt
from .schemas import QuestionAnswerModel
from backend.src.config import Config

load_dotenv()
api_key = Config.OPENAI_API_KEY
client = OpenAI(api_key=api_key)

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    try:
        response = client.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a {difficulty} difficulty coding challenge."}
            ],
            response_format=QuestionAnswerModel,
            temperature=0.7
        )
        print(type(json.loads(response.choices[0].message.content)))
        return json.loads(response.choices[0].message.content) #challenge_data

    except Exception as e:
        print(e)
        answer = QuestionAnswerModel(
            question="which is a basic Python list operation.",
            options=[
                    'my_list.append(5)', 
                    "my_list.add(5)", 
                    "my_list.push(5)", 
                    "my_list.insert(5)"
                    ],
            correct_answer_id=0,
            explanation="In Python, append() is the correct method to add an element to the end of a list."
            )
        return answer.model_dump()
    
if __name__ == "__main__":
    generate_challenge_with_ai()