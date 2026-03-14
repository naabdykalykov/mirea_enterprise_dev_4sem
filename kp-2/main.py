from fastapi import FastAPI
from data.products import sample_products
from models import UserCreate

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Авторелоад действительно работает"}


@app.post("/create_user")
def create_user(user: UserCreate):
    return user


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