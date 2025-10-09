from pydantic import BaseModel, Field


class ChallengeRequest(BaseModel):
    difficulty: str = Field(default="easy", examples=["easy"])


class QuestionAnswerModel(BaseModel):
    question: str = Field(description="The coding question the user can answer.")
    options: list[str] = Field(description="The options to choose from ", max_length=4, min_length=4)
    correct_answer_id: int = Field(description="The index of the correct answer (0-3) in the options list.")
    explanation: str = Field(description="A detailed explanation of why the correct answer is valid.")


class Step(BaseModel):
    explanation: str
    output: str