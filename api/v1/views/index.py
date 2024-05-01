#!/usr/bin/python3
"""
starts a Flask web application
"""

from models.engine.db_storage import classes
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
    for clas in classes:
        classes[clas] = storage.count(classes[clas])
    return jsonify(classes)