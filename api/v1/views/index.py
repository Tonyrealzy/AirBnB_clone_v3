#!/usr/bin/python3
"""Script that calls storage.close()"""


from flask import jsonify
from api.v1.views import app_views
from models import storage


# Create a route /status on the object app_views
@app_views.route('/status', methods=['GET'])
def get_status():
    """Return a JSON response"""
    return jsonify({"status": "OK"})


# Create an endpoint that retrieves the number
# of each objects by type
@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Return the number of each object by type"""
    stats = {}
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]

    for cls_name in classes:
        cls = storage.classes.get(cls_name)
        count = storage.count(cls)
        stats[cls_name] = count

    return jsonify(stats)