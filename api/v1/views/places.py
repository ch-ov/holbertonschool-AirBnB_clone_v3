#!/usr/bin/python3
""" places module for viewing their requests """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_by_city(city_id=None):
    """ view all places by city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places_list = []
    all_places = city.places
    for place in all_places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def place_by_id(place_id=None):
    """ view place by id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """ delete a place by id """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_places(city_id=None):
    """ returns a new place with status code 201 """
    requested_json = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not requested_json:
        abort(400, description="Not a JSON")
    if "user_id" not in requested_json:
        abort(400, description="Missing user_id")
    user = storage.get(User, requested_json.get('user_id'))
    if not user:
        abort(404)
    if "name" not in requested_json:
        abort(400, description="Missing name")
    requested_json["city_id"] = city_id
    new_place = Place(**requested_json)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id=None):
    """ update a place by id """
    place = storage.get(Place, place_id)
    requested_json = request.get_json()
    if not place:
        abort(404)
    if not requested_json:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in requested_json.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)
