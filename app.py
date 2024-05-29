from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import json
import os

app = FastAPI()

class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float

def read_json():
    try:
        if os.path.exists('db.json'):
            with open('db.json', 'r') as json_file:
                return json.load(json_file)
        else:
            return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def write_json(data):
    try:
        with open('db.json', 'w') as json_file:
            json.dump(data, json_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/products/{product_id}")
def read_product(product_id: str):
    try:
        products = read_json()
        if product_id in products.keys():
            return products[product_id]
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/products/")
def read_products():
    try:
        return read_json()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.put("/products/{product_id}")
def update_product(product_id: str, product: Product, response: Response):
    try:
        products = read_json()
        if product_id in products.keys():
            products[product_id] = product.dict()
            write_json(products)
            response.status_code = status.HTTP_200_OK
            return product.dict()
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/products/{product_id}")
def create_product(product_id: str, product: Product, response: Response):
    try:
        products = read_json()
        if product_id in products.keys():
            raise HTTPException(status_code=409, detail="Product already exists")
        else:
            products[product_id] = product.dict()
            write_json(products)
            response.status_code = status.HTTP_201_CREATED
            return product.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete("/products/{product_id}")
def delete_product(product_id: str, response: Response):
    try:
        products = read_json()
        if product_id in products.keys():
            del products[product_id]
            write_json(products)
            response.status_code = status.HTTP_200_OK
            return {"message": "Product deleted"}
        else:
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
