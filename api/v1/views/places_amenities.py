#!/usr/bin/python3
"""Creates for the link Place and Amenity objects"""
from flask import jsonify
from flask import request
from flask import abort
from flask import make_response
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.amenity import Amenity

@app_views('/places/<place_id>/amenities', methods=['GET'],
            strict_slashes=False)
def get_place_amenity(place_id):
    """Retrives the list of all Amenity of a Place"""
    if place_id is None:
        abort(404)

    place_value = storage.get('Place', place_id)
    if place_value is None:
        abort(404)

    # dictionary of all amneity objects
    amenity_dict = storage.all('Amenity')

    # amneity list
    amenity_list = []
    for amenity in amenity_dict.values():
        if amenity.place_id == place_id:
            amneity_list.append(amneity.to_dict())

    return make_response(jsonify(amneity_list), 200)    
