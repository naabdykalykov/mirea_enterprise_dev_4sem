from fastapi import FastAPI
from pathlib import Path
from fastapi.responses import HTMLResponse
from models import User, CalculateRequest, UserPayload, Feedback

app = FastAPI()
feedback_storage: list[Feedback] = []

@app.get("/")
def read_root():
    return {"message": "Авторелоад действительно работает"}
