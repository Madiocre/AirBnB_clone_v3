#!/usr/bin/python3
"""
starts a Flask web application
"""

from models.engine.db_storage import classe
from models import storage
from models.base_model import BaseModel
from flask import jsonify
from api.v1.views import app_views



@app_views.route("/status", strict_slashes=False)
def api_status():
    """  Returns JSON'd Text  """
    return jsonify(status='OK')


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ JSON """
    c = classe
    for clas in c:
        c[clas] = storage.count(c[clas])
    return jsonify(c)