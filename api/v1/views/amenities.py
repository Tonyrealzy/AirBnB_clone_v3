#!/usr/bin/python3
"""Amenities view module documentation is here!"""

# Import Flask and related modules
from flask import Flask, jsonify, abort, request

# Import the 'app_views' blueprint
from api.v1.views import app_views

# Import the necessary models
from models import storage
from models.amenity import Amenity

# Create a Flask application instance
app_views = Flask(__name__)

# Retrieve the list of all amenities
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])

# Retrieve a specific amenity by amenity_id
@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an Amenity object by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

# Delete an amenity by amenity_id
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

# Create a new amenity
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201

# Update an amenity by amenity_id
@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    # Ignore keys: id, created_at, and updated_at
    keys_to_ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200

if __name__ == "__main__":
    pass
