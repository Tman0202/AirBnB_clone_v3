#!/usr/bin/python3
"""used to manage blueprint"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes_dict = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
                "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """ returns json format status of api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrives the number of each object by type"""
    new_dict = {}
    for cls_name in classes_dict.keys():
        if cls_name == 'Amenity':
            new_dict['amenities'] = storage.count('Amenity')
        if cls_name == 'City':
            new_dict['cities'] = storage.count('City')
        if cls_name == 'Place':
            new_dict['places'] = storage.count('Place')
        if cls_name == 'Review':
            new_dict['reviews'] = storage.count('Review')
        if cls_name == 'State':
            new_dict['states'] = storage.count('State')
        if cls_name == 'User':
            new_dict['users'] = storage.count('User')
    return jsonify(new_dict)
