#!/usr/bin/python3
"""
states.py - Module for handling State objects in the API.

This module provides routes for managing State objects, including
retrieving all states, retrieving a specific state by ID, deleting a state,
creating a new state, and updating an existing state.

Routes:
    GET /states - Retrieves the list of all State objects.
    GET /states/<state_id> - Retrieves a specific State object by ID.
    DELETE /states/<state_id> - Deletes a State object by ID.
    POST /states - Creates a new State.
    PUT /states/<state_id> - Updates a State object by ID.

Usage:
    This module is part of the API's views and should be imported in the main app.

Example:
    from api.v1.views import states
    app.register_blueprint(states.app_views)
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


"""
Retrieves the list of all State objects.

Returns:
    JSON: A JSON response with the list of all State objects.
"""
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


"""
Retrieves the list of all State objects.

Returns:
    JSON: A JSON response with the list of all State objects.
"""
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


"""
Retrieves the list of all State objects.

Returns:
    JSON: A JSON response with the list of all State objects.
"""
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


"""
Retrieves the list of all State objects.

Returns:
    JSON: A JSON response with the list of all State objects.
"""
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


"""
Retrieves the list of all State objects.

Returns:
    JSON: A JSON response with the list of all State objects.
"""
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    # Ignore keys: id, created_at, and updated_at
    keys_to_ignore = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
