from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# ---------------------------
# Paths for data storage
# ---------------------------
HASH_FILE = "hash_store.json"
DATA_FILE = "causes.json"

# Ensure files exist
if not os.path.exists(HASH_FILE):
    with open(HASH_FILE, "w") as f:
        json.dump({}, f, indent=4)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f, indent=4)

# ---------------------------
# Utility functions
# ---------------------------
def load_hashes():
    with open(HASH_FILE, "r") as f:
        return json.load(f)

def save_hashes(data):
    with open(HASH_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------------
# Routes
# ---------------------------

# Home / Landing page
@app.route("/")
def home():
    return render_template("index.html")  # User connects MetaMask here

# Dash page (after clicking "Generate" on index.html)
@app.route("/dash")
def dash():
    return render_template("dash.html")  # Main dashboard page

# Admin page
@app.route("/admin")
def admin_page():
    return render_template("admin.html")

# API to store hash (if needed in future)
@app.route("/api/store-hash", methods=["POST"])
def store_hash():
    data = request.get_json()
    if not data or "hash" not in data:
        return jsonify({"error": "Invalid data"}), 400

    all_hashes = load_hashes()
    hash_key = data["hash"]
    all_hashes[hash_key] = {
        "address": data.get("address"),
        "timestamp": data.get("timestamp"),
        "nonce": data.get("nonce")
    }

    save_hashes(all_hashes)
    return jsonify({"message": "Hash stored successfully!"})

# Get all causes (for dashboard)
@app.route("/causes", methods=["GET"])
def get_causes():
    with open(DATA_FILE, "r") as f:
        causes = json.load(f)
    return jsonify(causes), 200

# Add new cause (admin only)
@app.route("/causes", methods=["POST"])
def add_cause():
    data = request.get_json()
    required_fields = ["title", "description", "goal", "image"]

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    with open(DATA_FILE, "r") as f:
        causes = json.load(f)

    new_cause = {
        "id": len(causes) + 1,
        "title": data["title"],
        "description": data["description"],
        "goal": data["goal"],
        "raised": 0,
        "image": data["image"]
    }

    causes.append(new_cause)

    with open(DATA_FILE, "w") as f:
        json.dump(causes, f, indent=4)

    return jsonify({"message": "Cause added successfully!", "cause": new_cause}), 201

# Serve static files (CSS, JS, images)
@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8000)
