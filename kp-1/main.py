from fastapi import FastAPI
from pathlib import Path
from fastapi.responses import HTMLResponse
from models import User, CalculateRequest

app = FastAPI()


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