#!/usr/bin/python3
"""Handles the default RESTFul API actions:"""

from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.user import User
import json


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all State objects"""
    new_list = []
    for user in storage.all('User').values():
        new_list.append(user.to_dict())
    return jsonify(new_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_one_user(user_id):
    """Retrives a single user"""
    user_value = storage.get('User', user_id)
    if user_value is None:
        abort(404)
    return jsonify(user_value.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_one_user(user_id):
    """deletes a single user"""
    user_value = storage.get('User', user_id)
    if user_value is None:
        abort(404)

    storage.delete(user_value)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_one_user():
    """creates a new user instance"""
    if request.get_json() is None:
        abort(404)

    content = request.get_json()
    if isinstance(content, dict) is False:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'email' not in content.keys():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in content.keys():
        return make_response(jsonify({"error": "Missing password"}), 400)

    for value in content.values():
        if isinstance(value, str) is False:
            abort(404)

    new_user = User(**content)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a user object"""
    if request.get_json() is None or user_id is None:
        abort(404)

    content = request.get_json()
    # checks if user input is a dictionary type
    if isinstance(content, dict) is False:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    user_value = storage.get('User', user_id)
    if user_value is None:
        abort(404)

    new_dict = user_value.to_dict()

    # checks if dictionary has only name as key and str value
    for key, value in content.items():
        if isinstance(value, str) is False:
            abort(404)
        if key == 'email':
            new_dict['email'] = value
        elif key == 'password':
            new_dict['password'] = value
        elif key == 'first_name':
            new_dict['first_name'] = value
        elif key == 'last_name':
            new_dict['last_name'] = value
        else:
            return make_response(jsonify({"error": "Not a JSON"}), 400)

    user_value.delete()
    user_value = User(**new_dict)
    user_value.save()
    return jsonify(user_value.to_dict())
