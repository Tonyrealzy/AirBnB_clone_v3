#!/usr/bin/python3
"""Initialize views package"""

from flask import Blueprint

# Create a variable app_views which is an instance of Blueprint
# (url prefix must be /api/v1)
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import specific names from each module
# Import the new file
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *


# Import the new view file
from api.v1.views import places_reviews

# Include other view files
from api.v1.views import states, cities, amenities, users, places

if __name__ == "__main__":
    pass
