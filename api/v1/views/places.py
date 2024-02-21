#!/usr/bin/python3
"""Places view module documentation is here!"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity

app_views = Flask(__name__)

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on the request JSON"""
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("Not a JSON")
        
        states = data.get('states', [])
        cities = data.get('cities', [])
        amenities = data.get('amenities', [])

        if not isinstance(states, list) or not isinstance(cities, list) or not isinstance(amenities, list):
            raise ValueError("Invalid JSON format")

        # Retrieve all places if the JSON body is empty
        if not states and not cities:
            places = storage.all(Place).values()
        else:
            places = []

            # Include places for each state
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    places.extend(state.places)

            # Include places for each city in states
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.extend(city.places)

            # Remove duplicates
            places = list(set(places))

        # Filter places based on amenities
        if amenities:
            filtered_places = []
            for place in places:
                place_amenities = {amenity.id for amenity in place.amenities}
                if set(amenities).issubset(place_amenities):
                    filtered_places.append(place)
            places = filtered_places

        return jsonify([place.to_dict() for place in places])

    except ValueError as e:
        abort(400, str(e))

if __name__ == "__main__":
    pass
