#!/usr/bin/python3
"""Initialize views package"""

from flask import Blueprint

# Create a variable app_views which is an instance of Blueprint
# (url prefix must be /api/v1)
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import specific names from each module
from api.v1.views.index import index
from api.v1.views.states import get_all_states, get_state, delete_state, create_state, update_state
from api.v1.views.cities import get_cities_by_state, get_city, delete_city, create_city, update_city
from api.v1.views.amenities import get_amenities, get_amenity, delete_amenity, create_amenity, update_amenity
from api.v1.views.users import get_users, get_user, delete_user, create_user, update_user
from api.v1.views.places import get_places_by_city, get_place, delete_place, create_place, update_place

# Import the new view file
from api.v1.views import places_reviews

# Include other view files
from api.v1.views import states, cities, amenities, users, places

if __name__ == "__main__":
    pass
