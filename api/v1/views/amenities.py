#!/usr/bin/python3
"""default views for RESTFul API"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """get a list of all Amenity object"""
    amenity_dict = storage.all('Amenity')
    amenity_list = []
    for amenity in amenity_dict.values():
        amenity_list.append(amenity.to_dict())
    return make_response(jsonify(amenity_list), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_an_amenity(amenity_id):
    """gets an amenity if it exists"""
    if amenity_id is None or isinstance(amenity_id, str) is False:
        abort(404)

    amenity_value = storage.get('Amenity', amenity_id)
    if amenity_value is None:
        abort(404)

    return make_response(jsonify(amenity_value.to_dict()), 200)

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_an_amenity(amenity_id):
    """deletes an amenity object"""

    if amenity_id is None or isinstance(amenity_id, str) is False:
        abort(404)

    amenity_value = storage.get('Amenity', amenity_id)
    if amenity_value is None:
        abort(404)

    storage.delete(amenity_value)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_an_amenity():
    """creates a new instance of an amenity object"""
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

    new_amenity = Amenity(**content)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_an_amenity(amenity_id):
    """Updates an instance of the Amenity object"""
    if request.get_json() is None or amenity_id is None:
        abort(404)

    content = request.get_json()
    # checks if user input is a dictionary type
    if isinstance(content, dict) is False:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    amenity_value = storage.get('Amenity', amenity_id)
    if amenity_value is None:
        abort(404)

    new_dict = amenity_value.to_dict()

    # checks if dictionary has only name as key and str value
    for key, value in content.items():
        if key != 'name':
            abort(404)
        if isinstance(value, str) is False:
            abort(404)
        new_dict['name'] = value

    amenity_value.delete()
    amenity_value = Amenity(**new_dict)
    amenity_value.save()
    return jsonify(amenity_value.to_dict())
