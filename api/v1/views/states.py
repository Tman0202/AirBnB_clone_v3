#!/usr/bin/python3
"""handles all default RESTFul API actions for state"""

from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.state import State
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    new_list = []
    for state in storage.all('State').values():
        new_list.append(state.to_dict())
    return jsonify(new_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_one_state(state_id):
    """Retrives a single state"""
    state_value = storage.get('State', state_id)
    if state_value is None:
        abort(404)
    return jsonify(state_value.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_state(state_id):
    """deletes a single state"""
    state_value = storage.get('State', state_id)
    if state_value is None:
        abort(404)

    city_dict = storage.all('City')
    for city in city_dict.values():
        if city.state_id == state_value.id:
            storage.delete(city)
    storage.delete(state_value)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_one_state():
    """creates a new state instance"""
    if request.get_json() is None:
        abort(404)

    content = request.get_json()
    if isinstance(content, dict) is False:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in content.items():
        if key != 'name':
            return make_response(jsonify({"error": "Missing name"}), 400)
        if isinstance(value, str) is False:
            abort(404)

    new_state = State(**content)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a state object"""
    if request.get_json() is None or state_id is None:
        abort(404)

    content = request.get_json()
    # checks if user input is a dictionary type
    if isinstance(content, dict) is False:
        return make_response(jsonify({"error": "Not a JSON"}), 404)

    state_value = storage.get('State', state_id)
    if state_value is None:
        abort(404)

    new_dict = state_value.to_dict()

    # checks if dictionary has only name as key and str value
    for key, value in content.items():
        if key != 'name':
            abort(404)
        if isinstance(value, str) is False:
            abort(404)
        new_dict['name'] = value

    state_value.delete()
    state_value = State(**new_dict)
    state_value.save()
    return jsonify(state_value.to_dict())
