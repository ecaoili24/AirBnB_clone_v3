#!/usr/bin/python3
"""A script that starts a Flask web application"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask import Blueprint
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(Error):
    """
    Creates a handler for 404 err that
    returns a JSON-formatted 404 status
    """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def app_teardown(self):
    """Removes current SQLAlchemy Session"""
    storage.close()

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST') or '0.0.0.0',
            port=os.getenv('HBNB_API_PORT') or '5000',
            threaded=True)
