#!/usr/bin/python3
""" amenities module for viewing their requests """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ view all amenities """
    all_amenities = storage.all(Amenity).values()
    amenities_list = []
    for amenity in all_amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_by_id(amenity_id=None):
    """ view amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """ delete an amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ returns a new amenity with status code 201 """
    requested_json = request.get_json()
    if not requested_json:
        abort(400, description="Not a JSON")
    if "name" not in requested_json:
        abort(400, description="Missing name")
    new_amenity = Amenity(**requested_json)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id=None):
    """ update an amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    requested_json = request.get_json()
    if not amenity:
        abort(404)
    if not requested_json:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in requested_json.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
