#!/usr/bin/python3
"""Status of API"""

from os import getenv
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """After each request remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """returns a JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
