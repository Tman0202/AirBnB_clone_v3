#!/usr/bin/python3
"""Handles all default RESTFul API actions for cities"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all places objects of a city"""
    if city_id is None:
        abort(404)

    city_value = storage.get('City', city_id)
    if city_value is None:
        abort(404)

    # dictionary of all place objects
    place_dict = storage.all('Place')

    # place list
    place_list = []
    for place in place_dict.values():
        if place.city_id == city_id:
            place_list.append(place.to_dict())

    return make_response(jsonify(place_list), 200)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_place(place_id):
    """Returns a place object with matching place_id"""
    # throws an error is no id is passes
    if place_id is None:
        abort(404)

    place_value = storage.get('Place', place_id)
    if place_value is None:
        abort(404)

    return make_response(jsonify(place_value.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_place(place_id):
    """Delete a place object"""
    # throws an error is no id is passed
    if place_id is None:
        abort(404)

    # find the object using the id and aborts if no object found
    place_value = storage.get('Place', place_id)
    if place_value is None:
        abort(404)

    storage.delete(place_value)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_one_place(city_id):
    """creates a new place instance"""
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    content = request.get_json()
    if isinstance(content, dict) is False:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'user_id' not in content.keys():
        return make_response(jsonify({"error": "Missing user_id"}), 400)

    if 'name' not in content.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)

    city_value = storage.get('City', city_id)
    if city_value is None:
        abort(404)

    user_value = storage.get('User', content.get('user_id'))
    if user_value is None:
        abort(404)

    content['city_id'] = city_value.id
    content['user_id'] = user_value.id
    new_place = Place(**content)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a state object"""
    if place_id is None:
        abort(404)

    content = request.get_json()
    # checks if user input is a dictionary type
    if isinstance(content, dict) is False or request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    place_value = storage.get('Place', place_id)
    if place_value is None:
        abort(404)

    new_dict = place_value.to_dict()

    # checks if dictionary has only name as key and str value
    for key, value in content.items():
        if key == 'name':
            if isinstance(value, str) is True:
                new_dict['name'] = value
        elif key == 'description':
            if isinstance(value, str) is True:
                new_dict['description'] = value
        elif key == 'number_rooms':
            if isinstance(value, int) is True:
                new_dict['number_rooms'] = value
        elif key == 'number_bathrooms':
            if isinstance(value, int) is True:
                new_dict['number_bathrooms'] = value
        elif key == 'max_guest':
            if isinstance(value, int) is True:
                new_dict['max_guest'] = value
        elif key == 'price_by_night':
            if isinstance(value, int) is True:
                new_dict['price_by_night'] = value
        elif key == 'latitude':
            if isinstance(value, float) is True:
                new_dict['latitude'] = value
        elif key == 'longtiude':
            if isinstance(value, float) is True:
                new_dict['longtiude'] = value
        else:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

    place_value.delete()
    place_value = Place(**new_dict)
    place_value.save()
    return jsonify(place_value.to_dict())
