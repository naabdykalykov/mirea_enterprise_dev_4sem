from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from itsdangerous import BadSignature, Signer

from data.products import sample_products
from models import UserCreate

app = FastAPI()

_USERS_DB: dict[str, dict[str, object]] = {
    "user123": {"password": "password123", "full_name": "User 123", "role": "user"},
    "admin": {"password": "admin123", "full_name": "Admin", "role": "admin"},
}

_SESSIONS: dict[str, str] = {}


_SECRET_KEY = "dev-secret-key-change-me"
_signer = Signer(_SECRET_KEY)
_COOKIE_MAX_AGE_SECONDS = 60 * 15

_USER_IDS: dict[str, str] = {}


def _unauthorized() -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": "Unauthorized"})


async def _extract_login_credentials(request: Request) -> tuple[str, str]:
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        payload = await request.json()
        username = payload.get("username")
        password = payload.get("password")
    else:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        raise HTTPException(status_code=400, detail="username and password are required")

    return username, password


@app.get("/")
def read_root():
    return {"message": "Авторелоад действительно работает"}


@app.post("/create_user")
def create_user(user: UserCreate):
    return user


@app.post("/login")
async def login(request: Request, response: Response):
    username, password = await _extract_login_credentials(request)

    user = _USERS_DB.get(username)
    if user is None or user.get("password") != password:
        return _unauthorized()

    user_id = str(uuid4())
    session_token = _signer.sign(user_id).decode("utf-8")
    _USER_IDS[user_id] = username

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=_COOKIE_MAX_AGE_SECONDS,
    )

    return {"message": "Logged in"}


@app.get("/user")
def get_user_profile(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        return _unauthorized()

    try:
        user_id = _signer.unsign(session_token).decode("utf-8")
    except BadSignature:
        return _unauthorized()

    username = _USER_IDS.get(user_id)
    if not username:
        return _unauthorized()

    user = _USERS_DB.get(username)
    if not user:
        return _unauthorized()

    return {
        "username": username,
        "full_name": user.get("full_name"),
        "role": user.get("role"),
    }


@app.get("/profile")
def profile(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        return _unauthorized()

    try:
        user_id = _signer.unsign(session_token).decode("utf-8")
    except BadSignature:
        return _unauthorized()

    username = _USER_IDS.get(user_id)
    if not username:
        return _unauthorized()

    user = _USERS_DB.get(username)
    if not user:
        return _unauthorized()

    return {
        "user_id": user_id,
        "username": username,
        "full_name": user.get("full_name"),
        "role": user.get("role"),
    }


@app.get("/product/{product_id}")
def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product

    return {"error": "Product not found"}

@app.get("/products/search")
def search_products(
    keyword: str,
    category: str | None = None,
    limit: int = 10,
):
    keyword_lower = keyword.lower()
    filtered_products = []
    for product in sample_products:
        name_lower = product["name"].lower()

        if keyword_lower not in name_lower:
            continue

        if category is not None and product["category"] != category:
            continue

        filtered_products.append(product)

    return filtered_products[:limit]