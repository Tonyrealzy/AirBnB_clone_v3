#!/usr/bin/python3
"""Script that calls storage.close()"""


from flask import jsonify
from api.v1.views import app_views


# Create a route /status on the object app_views
@app_views.route('/status', methods=['GET'])
def get_status():
    """Return a JSON response"""
    return jsonify({"status": "OK"})
