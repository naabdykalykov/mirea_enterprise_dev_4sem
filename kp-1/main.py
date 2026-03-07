from fastapi import FastAPI
from pathlib import Path
from fastapi.responses import HTMLResponse
from models import User, CalculateRequest, UserPayload, Feedback

app = FastAPI()
feedback_storage: list[Feedback] = []

@app.get("/")
def read_root():
    return {"message": "Авторелоад действительно работает"}


TEMPLATES_DIR = Path(__file__).parent / "templates"
INDEX_HTML = TEMPLATES_DIR / "index.html"


@app.get("/first-class", response_class=HTMLResponse)
def read_first_class_root():
    return INDEX_HTML.read_text(encoding="utf-8")

@app.post("/calculate")
def calculate(data: CalculateRequest):
    return {"result": data.num1 + data.num2}

current_user = User(name="Nursultan", id=1)

@app.get("/users")
def get_users():
    return current_user

def is_adult(age: int) -> bool:
    return age >= 18

@app.post("/user")
def create_user(data: UserPayload):
    adult = is_adult(data.age)
    return {
        "name": data.name,
        "age": data.age,
        "is_adult": adult
    }

@app.post("/feedback")
def post_feedback(data: Feedback):
    feedback_storage.append(data)
    return {"message": f"Feedback received. Thank you, {data.name}."}

@app.get("/feedback", response_model=list[Feedback])
def get_feedback():
    return feedback_storage