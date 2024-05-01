#!/usr/bin/python3
"""
starts a Flask web application
"""

from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views



@app_views.route("/status", strict_slashes=False)
def api_status():
    """  Returns JSON'd Text  """
    return jsonify(status='OK')


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    """ JSON """
    classes = {"amenity": Amenity, "city": City,
          "place": Place, "review": Review, "state": State, "user": User}
    for clas in classes:
        classes[clas] = storage.count(classes[clas])
    return jsonify(classes)