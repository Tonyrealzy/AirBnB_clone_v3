#!/usr/bin/python3
"""Users view module documentation is here!"""

# Import Flask and related modules
from flask import Flask, jsonify, abort, request

# Import the 'app_views' blueprint
from api.v1.views import app_views

# Import the necessary models
from models import storage
from models.user import User

# Create a Flask application instance
app_views = Flask(__name__)

# Retrieve the list of all users
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

# Retrieve a specific user by user_id
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object by user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

# Delete a user by user_id
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object by user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

# Create a new user
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400

    new_user = User(**data)
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201

# Update a user by user_id
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object by user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    # Ignore keys: id, email, created_at, and updated_at
    keys_to_ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200

if __name__ == "__main__":
    pass
