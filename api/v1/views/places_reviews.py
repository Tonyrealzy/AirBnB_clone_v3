#!/usr/bin/python3
"""_summary_

    Returns:
        _type_: _description_
"""

# Import Flask and related modules
from flask import Flask, jsonify, abort, request

# Import the 'app_views' blueprint
from api.v1.views import app_views

# Import the necessary models
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

# Create a Flask application instance
app_views = Flask(__name__)

# Retrieve the list of reviews for a specific place
@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

# Retrieve a specific review by review_id
@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())

# Delete a review by review_id
@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

# Create a new review for a specific place
@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    new_review = Review(place_id=place_id, **data)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201

# Update a review by review_id
@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    # Ignore keys: id, user_id, place_id, created_at, and updated_at
    keys_to_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
