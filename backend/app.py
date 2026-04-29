from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

DUMMYJSON_BASE = "https://dummyjson.com"
USERNAME = "emilys"
PASSWORD = "emilyspass"

access_token = None


def login_to_dummyjson():
    global access_token
    resp = requests.post(
        f"{DUMMYJSON_BASE}/user/login",
        json={
            "username": USERNAME,
            "password": PASSWORD,
            "expiresInMins": 30,
        },
    )
    if resp.status_code != 200:
        return None
    data = resp.json()
    access_token = data.get("accessToken")
    return access_token


def get_auth_headers():
    global access_token
    if not access_token:
        token = login_to_dummyjson()
        if not token:
            return None
    return {"Authorization": f"Bearer {access_token}"}


@app.route("/api/token", methods=["GET"])
def get_token():
    global access_token
    if not access_token:
        token = login_to_dummyjson()
        if not token:
            return jsonify({"error": "Failed to login to DummyJSON"}), 500
    return jsonify({"accessToken": access_token})


@app.route("/api/products", methods=["GET"])
def get_products():
    """
    Optional query params:
      - q: search term
      - limit: number of items
    """
    headers = get_auth_headers()
    if headers is None:
        return jsonify({"error": "Auth failed"}), 500

    q = request.args.get("q")
    limit = request.args.get("limit", "10")

    if q:
        url = f"{DUMMYJSON_BASE}/products/search?q={q}&limit={limit}"
    else:
        url = f"{DUMMYJSON_BASE}/products?limit={limit}"

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return jsonify({"error": "Failed to fetch products"}), 500

    data = resp.json()
    products = data.get("products", [])
    return jsonify({"products": products})


@app.route("/api/users", methods=["GET"])
def get_users():
    """
    Optional query params:
      - q: search term (we'll filter client-side-like on name/username)
      - limit: number of items
    """
    headers = get_auth_headers()
    if headers is None:
        return jsonify({"error": "Auth failed"}), 500

    limit = request.args.get("limit", "20")
    q = request.args.get("q", "").lower()

    url = f"{DUMMYJSON_BASE}/users?limit={limit}"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return jsonify({"error": "Failed to fetch users"}), 500

    data = resp.json()
    users = data.get("users", [])

    if q:
        def matches(u):
            full_name = f"{u.get('firstName', '')} {u.get('lastName', '')}".lower()
            username = u.get("username", "").lower()
            return q in full_name or q in username

        users = [u for u in users if matches(u)]

    return jsonify({"users": users})


@app.route("/api/dashboard", methods=["GET"])
def get_dashboard():
    """
    Combined dashboard endpoint:
      - optional qProducts, qUsers
    """
    headers = get_auth_headers()
    if headers is None:
        return jsonify({"error": "Auth failed"}), 500

    q_products = request.args.get("qProducts")
    q_users = request.args.get("qUsers")

    # products
    if q_products:
        products_url = f"{DUMMYJSON_BASE}/products/search?q={q_products}&limit=20"
    else:
        products_url = f"{DUMMYJSON_BASE}/products?limit=20"

    products_resp = requests.get(products_url, headers=headers)

    # users
    users_url = f"{DUMMYJSON_BASE}/users?limit=50"
    users_resp = requests.get(users_url, headers=headers)

    if products_resp.status_code != 200 or users_resp.status_code != 200:
        return jsonify({"error": "Failed to fetch dashboard data"}), 500

    products = products_resp.json().get("products", [])
    users = users_resp.json().get("users", [])

    if q_users:
        ql = q_users.lower()

        def matches(u):
            full_name = f"{u.get('firstName', '')} {u.get('lastName', '')}".lower()
            username = u.get("username", "").lower()
            return ql in full_name or ql in username

        users = [u for u in users if matches(u)]

    return jsonify({
        "products": products,
        "users": users,
        "summary": {
            "totalProducts": len(products),
            "totalUsers": len(users),
        },
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

