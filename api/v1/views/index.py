#!/usr/bin/python3
"""
starts a Flask web application
"""

import models
from models import storage
from models.base_model import BaseModel
from flask import Flask, jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False


@app_views.route("/status")
def api_status():
    """  Returns JSON'd Text  """
    return jsonify(status='OK')


@app_views.route("/stats")
def get_stats():
    """ JSON """
    data = {'states': State, 'users': User,
            'amenities': Amenity, 'cities': City,
            'places': Place, 'reviews': Review}
    for item in data:
        data[item] = storage.count(data[item])
    return jsonify(data)
