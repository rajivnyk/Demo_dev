from flask import Flask, request, jsonify

from config import Config
from models import db, User


app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Connect SQLAlchemy to Flask
db.init_app(app)


# Create database tables
with app.app_context():
    db.create_all()


# -------------------------
# HOME
# -------------------------

@app.route("/")
def home():
    return jsonify({
        "message": "Flask + MySQL + SQLAlchemy is working!"
    })


# -------------------------
# GET ALL USERS
# -------------------------

@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    return jsonify([
        user.to_dict()
        for user in users
    ])


# -------------------------
# GET ONE USER
# -------------------------

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify(user.to_dict())


# -------------------------
# CREATE USER
# -------------------------

@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "error": "Name and email are required"
        }), 400

    # Check whether email already exists
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "error": "Email already exists"
        }), 409

    user = User(
        name=name,
        email=email
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": user.to_dict()
    }), 201


# -------------------------
# UPDATE USER
# -------------------------

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if name:
        user.name = name

    if email:

        existing_user = User.query.filter(
            User.email == email,
            User.id != user_id
        ).first()

        if existing_user:
            return jsonify({
                "error": "Email already exists"
            }), 409

        user.email = email

    db.session.commit()

    return jsonify({
        "message": "User updated successfully",
        "user": user.to_dict()
    })


# -------------------------
# DELETE USER
# -------------------------

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "User deleted successfully"
    })


# -------------------------
# RUN APPLICATION
# -------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )