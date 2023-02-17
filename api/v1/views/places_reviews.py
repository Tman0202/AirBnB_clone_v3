#!/usr/bin/python3
"""Handles all default RESTFul API actions for cities"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all review objects of a place"""
    if place_id is None:
        abort(404)

    place_value = storage.get('Place', place_id)
    if place_value is None:
        abort(404)

    # dictionary of all review objects
    review_dict = storage.all('Review')

    # review list
    review_list = []
    for review in review_dict.values():
        if review.place_id == place_id:
            review_list.append(review.to_dict())

    return make_response(jsonify(review_list), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_review(review_id):
    """Returns a review object with matching review_id"""
    # throws an error is no id is passes
    if review_id is None:
        abort(404)

    review_value = storage.get('Review', review_id)
    if review_value is None:
        abort(404)

    return make_response(jsonify(review_value.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_review(review_id):
    """Delete a review object"""
    # throws an error is no id is passed
    if review_id is None:
        abort(404)

    # find the object using the id and aborts if no object found
    review_value = storage.get('Review', review_id)
    if review_value is None:
        abort(404)

    storage.delete(review_value)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_one_review(place_id):
    """creates a new review instance"""
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    content = request.get_json()
    if isinstance(content, dict) is False:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    place_value = storage.get('Place', place_id)
    if place_value is None:
        abort(404)

    if 'user_id' not in content.keys():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in content.keys():
        return make_response(jsonify({"error": "Missing text"}), 400)

    user_value = storage.get('User', content.get('user_id'))
    if user_value is None:
        abort(404)

    content['place_id'] = place_id
    new_review = Review(**content)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a review object"""
    if review_id is None:
        abort(404)

    content = request.get_json()
    # checks if user input is a dictionary type
    if isinstance(content, dict) is False or request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    review_value = storage.get('Review', review_id)
    if review_value is None:
        abort(404)

    new_dict = review_value.to_dict()

    # checks if dictionary has only name as key and str value
    for key, value in content.items():
        if key != 'text':
            return make_response(jsonify({"error": "Not a JSON"}), 400)

    new_dict['text'] = content.get('text')
    review_value.delete()
    review_value = Review(**new_dict)
    review_value.save()
    return jsonify(review_value.to_dict())
