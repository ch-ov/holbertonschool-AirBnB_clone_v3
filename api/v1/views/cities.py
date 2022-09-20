#!/usr/bin/python3
"""create new view for City objects that handles default RESTFul API actions"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route('/api/v1/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/api/v1/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/api/v1/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Creates a City"""
    post_city = request.get_json()
    if not storage.get("State", state_id):
        abort(404)
    if not post_city:
        abort(400, {"Not a JSON"})
    elif 'name' not in post_city:
        abort(400, {"Missing name"})
    post_city['state_id'] = state_id
    new_city = request.get_json()
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/api/v1/cities/<city_id>',
                 strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    if not request.get_json():
        abort(400, {"Not a JSON"})
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
