from fastapi import FastAPI

# 1.create instance of FsatAPI class
app = FastAPI()

# ===============================================
# 2. decorator to define the root endpoint

@app.get("/")
def index():
    return {"message": "Hello, there!"}

@app.get("/property")
def property():
    return "This is a property page!"

# ===============================================
# 3. Path Parameter

# int parameter
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {f'This is item number {item_id}'}


# string parameter
@app.get("/users/{username}")
def read_username(username: str):
    return {f"This is the username: {username}"}

# ================================================
# 4. Query Parameter

# Query parameters are "optional" by default, so you can define them with a default value. Also, they can be of any type. 
# - They come after the ? in the URL.
# - Multiple parameters are separated by &. (GET /items?skip=0&limit=10&search=book)
# Use cases = Filtering, pagination, search queries

# http://127.0.0.1:8000/products/?id=1&price=100

# Works fine with or without query parameters, because we had set default values
# http://127.0.0.1:8000/products/
@app.get("/products/")
def products(id:int=1, price:int=0):
    return {f'This is the product id: {id} and price {price}'}


# ===============================================

# 5. using both path and query parameters together
# http://127.0.0.1:8000/products/10/order_id?order_id=20

@app.get("/products/{product_id}/order_id")
def get_product(product_id:int, order_id:int=1):
    return {f"This is the product id {product_id} and order id {order_id}"}


# ===============================================

# 6. Required Query Parameters, when no default value is provided and make sure no error is thrown.
# http://127.0.0.1:8000/orders/1/order_id

@app.get("/orders/{product_id}/order_id")
def get_orders(product_id:int=None, order_id:int=None):
    return {f"This is the product id {product_id} and order id {order_id}"}
