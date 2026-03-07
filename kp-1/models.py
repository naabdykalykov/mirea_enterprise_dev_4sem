from pydantic import BaseModel


class User(BaseModel):
    name: str
    id: int


class CalculateRequest(BaseModel):
    num1: float
    num2: float