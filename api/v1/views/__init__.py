from flask import Blueprint

# Create a variable app_views which is an instance of Blueprint
# (url prefix must be /api/v1)
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import of everything in the package api.v1.views.index
# PEP8 will complain about it, don’t worry, it’s normal
# and this file (v1/views/__init__.py) won’t be checked.

# Import the views module
from . import index
