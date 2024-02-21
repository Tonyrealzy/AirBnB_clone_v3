#!/usr/bin/python3
"""_summary_"""


import os
from flask import Flask
from models import storage
from api.v1.views import app_views

# Create a FLask instance
app = Flask(__name__)

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# Declare a method to handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_appcontext(error):
    storage.close()

if __name__ == "__main__":
    # Run your Flask server (variable app)
    # Define host and port based on environment variables or defaults
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
