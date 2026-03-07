from fastapi import FastAPI
from pathlib import Path
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Авторелоад действительно работает"}


TEMPLATES_DIR = Path(__file__).parent / "templates"
INDEX_HTML = TEMPLATES_DIR / "index.html"


@app.get("/first-class", response_class=HTMLResponse)
def read_first_class_root():
    return INDEX_HTML.read_text(encoding="utf-8")
