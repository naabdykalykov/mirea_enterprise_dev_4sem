from pydantic import BaseModel


class User(BaseModel):
    name: str
    id: int


class UserPayload(BaseModel):
    name: str
    age: int


class CalculateRequest(BaseModel):
    num1: float
    num2: float

class Feedback(BaseModel):
    name: str
    message: str