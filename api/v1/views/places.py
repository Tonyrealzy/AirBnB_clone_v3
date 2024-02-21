#!/usr/bin/python3
"""Places view module documentation is here!"""

# Import Flask and related modules
from flask import Flask, jsonify, abort, request

# Import the 'app_views' blueprint
from api.v1.views import app_views

# Import the necessary models
from models import storage
from models.place import Place
from models.user import User
from models.city import City

# Create a Flask application instance
app_views = Flask(__name__)

# Retrieve the list of all places for a specific city
@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

# Retrieve a specific place by place_id
@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

# Delete a place by place_id
@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

# Create a new place for a specific city
@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    new_place = Place(city_id=city_id, user_id=data['user_id'], **data)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201

# Update a place by place_id
@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    # Ignore keys: id, user_id, city_id, created_at, and updated_at
    keys_to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200

if __name__ == "__main__":
    pass
