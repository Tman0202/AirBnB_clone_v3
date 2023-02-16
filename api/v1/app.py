#!/usr/bin/python3
"""root for api"""

from flask import Flask
from flask import Blueprint
from flask import jsonify
from flask import make_response
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """method to handle closure"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    if os.getenv('HBNB_API_HOST') is not None:
        Host = os.getenv('HBNB_API_HOST')
    else:
        Host = '0.0.0.0'

    if os.getenv('HBNB_API_PORT') is not None:
        Port = os.getenv('HBNB_API_PORT')
    else:
        Port = '5000'

    app.run(host=Host, port=Port, threaded=True)
