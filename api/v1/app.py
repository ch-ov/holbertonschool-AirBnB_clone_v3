#!/usr/bin/python3
"""Status of API"""

from os import getenv
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """After each request remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """returns a JSON-formatted 404 status code response"""
    error_mssg = {"error": "Not found"}
    return make_response(jsonify(error_mssg), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
