from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------
# 20 MOCK PRODUCTS
# ---------------------------------------------------------
MOCK_PRODUCTS = [
    {"id": 1, "title": "iPhone 9", "brand": "Apple", "price": 549, "rating": 4.69},
    {"id": 2, "title": "Samsung Universe 9", "brand": "Samsung", "price": 1249, "rating": 4.09},
    {"id": 3, "title": "MacBook Pro", "brand": "Apple", "price": 1749, "rating": 4.57},
    {"id": 4, "title": "Huawei P30", "brand": "Huawei", "price": 499, "rating": 4.3},
    {"id": 5, "title": "OPPO F19", "brand": "OPPO", "price": 280, "rating": 4.3},
    {"id": 6, "title": "HP Pavilion 15", "brand": "HP", "price": 1099, "rating": 4.5},
    {"id": 7, "title": "Dell XPS 13", "brand": "Dell", "price": 1299, "rating": 4.6},
    {"id": 8, "title": "Sony WH‑1000XM4", "brand": "Sony", "price": 349, "rating": 4.8},
    {"id": 9, "title": "Canon EOS 80D", "brand": "Canon", "price": 999, "rating": 4.7},
    {"id": 10, "title": "Nikon D3500", "brand": "Nikon", "price": 649, "rating": 4.6},
    {"id": 11, "title": "Google Pixel 6", "brand": "Google", "price": 599, "rating": 4.5},
    {"id": 12, "title": "Asus ROG Phone 5", "brand": "Asus", "price": 999, "rating": 4.7},
    {"id": 13, "title": "Lenovo ThinkPad X1", "brand": "Lenovo", "price": 1399, "rating": 4.8},
    {"id": 14, "title": "Acer Predator Helios", "brand": "Acer", "price": 1499, "rating": 4.6},
    {"id": 15, "title": "Xiaomi Mi 11", "brand": "Xiaomi", "price": 749, "rating": 4.4},
    {"id": 16, "title": "OnePlus 9 Pro", "brand": "OnePlus", "price": 969, "rating": 4.5},
    {"id": 17, "title": "LG Gram 17", "brand": "LG", "price": 1799, "rating": 4.7},
    {"id": 18, "title": "Razer Blade 15", "brand": "Razer", "price": 1999, "rating": 4.6},
    {"id": 19, "title": "Beats Studio 3", "brand": "Beats", "price": 349, "rating": 4.4},
    {"id": 20, "title": "JBL Charge 5", "brand": "JBL", "price": 179, "rating": 4.7},
]

# ---------------------------------------------------------
# 20 MOCK USERS
# ---------------------------------------------------------
MOCK_USERS = [
    {"id": 1, "firstName": "Emily", "lastName": "Johnson", "username": "emilys", "age": 28, "address": {"city": "New York"}},
    {"id": 2, "firstName": "Michael", "lastName": "Smith", "username": "mikes", "age": 34, "address": {"city": "Chicago"}},
    {"id": 3, "firstName": "Sarah", "lastName": "Lee", "username": "sarahlee", "age": 25, "address": {"city": "Los Angeles"}},
    {"id": 4, "firstName": "David", "lastName": "Brown", "username": "daveb", "age": 42, "address": {"city": "Houston"}},
    {"id": 5, "firstName": "Sophia", "lastName": "Martinez", "username": "sophiam", "age": 30, "address": {"city": "Phoenix"}},
    {"id": 6, "firstName": "James", "lastName": "Davis", "username": "jimd", "age": 37, "address": {"city": "Philadelphia"}},
    {"id": 7, "firstName": "Olivia", "lastName": "Garcia", "username": "oliviag", "age": 26, "address": {"city": "San Antonio"}},
    {"id": 8, "firstName": "Daniel", "lastName": "Rodriguez", "username": "danrod", "age": 33, "address": {"city": "San Diego"}},
    {"id": 9, "firstName": "Ava", "lastName": "Wilson", "username": "avaw", "age": 22, "address": {"city": "Dallas"}},
    {"id": 10, "firstName": "Ethan", "lastName": "Anderson", "username": "ethana", "age": 29, "address": {"city": "San Jose"}},
    {"id": 11, "firstName": "Isabella", "lastName": "Thomas", "username": "isabellat", "age": 31, "address": {"city": "Austin"}},
    {"id": 12, "firstName": "Matthew", "lastName": "Taylor", "username": "mattt", "age": 40, "address": {"city": "Jacksonville"}},
    {"id": 13, "firstName": "Mia", "lastName": "Moore", "username": "miam", "age": 24, "address": {"city": "Fort Worth"}},
    {"id": 14, "firstName": "Alexander", "lastName": "Harris", "username": "alexh", "age": 35, "address": {"city": "Columbus"}},
    {"id": 15, "firstName": "Charlotte", "lastName": "Clark", "username": "charlottec", "age": 27, "address": {"city": "Charlotte"}},
    {"id": 16, "firstName": "Benjamin", "lastName": "Lewis", "username": "benl", "age": 32, "address": {"city": "San Francisco"}},
    {"id": 17, "firstName": "Amelia", "lastName": "Walker", "username": "ameliaw", "age": 23, "address": {"city": "Indianapolis"}},
    {"id": 18, "firstName": "Henry", "lastName": "Hall", "username": "henryh", "age": 38, "address": {"city": "Seattle"}},
    {"id": 19, "firstName": "Evelyn", "lastName": "Young", "username": "evelyny", "age": 29, "address": {"city": "Denver"}},
    {"id": 20, "firstName": "Lucas", "lastName": "King", "username": "lucask", "age": 36, "address": {"city": "Washington"}},
]

# ---------------------------------------------------------
# API ENDPOINTS
# ---------------------------------------------------------

@app.route("/api/token")
def get_token():
    return jsonify({"accessToken": "mock-token-123"})


@app.route("/api/products")
def get_products():
    return jsonify({"products": MOCK_PRODUCTS})


@app.route("/api/users")
def get_users():
    return jsonify({"users": MOCK_USERS})


@app.route("/api/product/<int:product_id>")
def get_product(product_id):
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)


@app.route("/api/user/<int:user_id>")
def get_user(user_id):
    user = next((u for u in MOCK_USERS if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@app.route("/api/dashboard")
def dashboard():
    return jsonify({
        "products": MOCK_PRODUCTS,
        "users": MOCK_USERS,
        "summary": {
            "totalProducts": len(MOCK_PRODUCTS),
            "totalUsers": len(MOCK_USERS)
        }
    })


if __name__ == "__main__":
    app.run(port=8000, debug=True)
