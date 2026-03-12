from fastapi import FastAPI

from models import UserCreate

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Авторелоад действительно работает"}


@app.post("/create_user")
def create_user(user: UserCreate):
    return user
