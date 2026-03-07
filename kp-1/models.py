from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    name: str
    id: int


class UserPayload(BaseModel):
    name: str
    age: int


class CalculateRequest(BaseModel):
    num1: float
    num2: float

FORBIDDEN_WORDS = ("кринж", "рофл", "вайб")

class Feedback(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=10, max_length=500)

    @field_validator("message")
    @classmethod
    def message_no_forbidden_words(cls, v: str) -> str:
        lower = v.lower()
        for word in FORBIDDEN_WORDS:
            if word in lower:
                raise ValueError("Использование недопустимых слов")
        return v
    

