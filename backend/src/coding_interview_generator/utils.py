import os
import json

from openai import OpenAI
from typing import Dict, Any
from dotenv import load_dotenv

from .prompts import system_prompt
from .schemas import QuestionAnswerModel
from src.config import Config

load_dotenv()
api_key = Config.OPENAI_API_KEY
client = OpenAI(api_key=api_key)

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a {difficulty} difficulty coding challenge."}
            ],
            text_format=QuestionAnswerModel,
            temperature=0.7
        )

        challenge_data  = response.output_parsed

        required_fields = ("question", "options", "correct_answer_id", "explanation")
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")

        return challenge_data

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