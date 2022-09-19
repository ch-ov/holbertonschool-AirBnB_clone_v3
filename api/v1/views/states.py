#!/usr/bin/python3
""" module retrieve information from states """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ view all states """
    states_list = []
    for i in storage.all(State).values():
        states_list.append(i.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id=None):
    """ view state by id """
    try:
        state = storage.get(State, state_id)
        return jsonify(state.to_dict())
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id=None):
    """ del state by id """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ returns a new state with status code 201 """
    requested_json = request.get_json()
    if not requested_json:
        abort(400, description="Not a JSON")
    if "name" not in requested_json:
        abort(400, description="Missing name")
    new_state = State(**requested_json)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    """ update a state by id """
    state = storage.get(State, state_id)
    requested_json = request.get_json()
    if not state:
        abort(404)
    if not requested_json:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in requested_json.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
