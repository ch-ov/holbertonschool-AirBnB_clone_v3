#!/usr/bin/python3
"""Index to check status"""

from flask import Flask
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
        }


@app_views.route('/api/v1/status', strict_slashes=False)
def status():
    """Return status: OK"""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', strict_slashes=False)
def count_cls():
    """ Counts each staorage class """
    cls_dict = {}
    for k, v in classes.items():
        cls_dict[k] = storage.count(v)

    return jsonify(cls_dict)
