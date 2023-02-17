#!/usr/bin/python3
"""Handles all default RESTFul API actions for cities"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    if state_id is None:
        abort(404)

    state_value = storage.get('State', state_id)
    if state_value is None:
        abort(404)

    # dictionary of all city objects
    city_dict = storage.all('City')

    # city list
    city_list = []
    for city in city_dict.values():
        if city.state_id == state_id:
            city_list.append(city.to_dict())

    return make_response(jsonify(city_list), 200)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_city(city_id):
    """Returns a city object with matching city_id"""
    # throws an error is no id is passes
    if city_id is None:
        abort(404)

    city_value = storage.get('City', city_id)
    if city_value is None:
        abort(404)

    return make_response(jsonify(city_value.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_city(city_id):
    """Delete a city object"""
    # throws an error is no id is passed
    if city_id is None:
        abort(404)

    # find the object using the id and aborts if no object found
    city_value = storage.get('City', city_id)
    if city_value is None:
        abort(404)

    storage.delete(city_value)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_one_city(state_id):
    """creates a new state instance"""
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    content = request.get_json()
    if isinstance(content, dict) is False:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in content.items():
        if key != 'name':
            return make_response(jsonify({"error": "Missing name"}), 400)
        if isinstance(value, str) is False:
            abort(404)

    state_value = storage.get('State', state_id)
    if state_value is None:
        abort(404)

    content['state_id'] = state_id
    new_city = City(**content)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a state object"""
    if city_id is None:
        abort(404)

    content = request.get_json()
    # checks if user input is a dictionary type
    if isinstance(content, dict) is False or request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    city_value = storage.get('City', city_id)
    if city_value is None:
        abort(404)

    new_dict = city_value.to_dict()

    # checks if dictionary has only name as key and str value
    for key, value in content.items():
        if key != 'name':
            abort(404)
        if isinstance(value, str) is False:
            abort(404)
        new_dict['name'] = value

    city_value.delete()
    city_value = City(**new_dict)
    city_value.save()
    return jsonify(city_value.to_dict())
