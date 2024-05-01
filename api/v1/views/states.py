#!/usr/bin/python3
"""
Init.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app_views.route("/states", methods=['GET'])
def states():
    """States endpoint."""
    states = storage.all('State')
    listed = []
    for state in states.values():
        listed.append(state.to_dict())
    return jsonify(listed)


@app_views.route('/states/<state>', methods=['GET'])
def statebyid(state):
    """States endpoint."""
    state = storage.get('State', state)
    if state is None:
        abort(404)
    return jsonify(state.to_dict(), 200)


@app_views.route('/states/', methods=['POST'])
def setstate():
    """States endpoint."""
    if not request.json:
        abort(400, {'Not a JSON'})
    if "name" not in request.get_json():
        abort(400, {'Missing name'})
    toset = State(**request.get_json())
    storage.new(toset)
    storage.save()
    return jsonify(toset.to_dict()), '201'


@app_views.route('/states/<state_id>', methods=['PUT'])
def upstate(state_id):
    """States endpoint."""
    if not request.json:
        abort(400, {'Not a JSON'})
    toupdate = storage.get(State, state_id)
    if toupdate is None:
        abort(404)
    dkey = ['id', 'created_at', 'updated_at']
    for key, val in request.json.items():
        if key not in dkey:
            setattr(toupdate, key, val)
    toupdate.save()
    return jsonify(toupdate.to_dict()), '200'


@app_views.route('/states/<state_id>', methods=['DELETE'])
def deleting(state_id):
    """States endpoint."""
    todelete = storage.get(State, state_id)
    if todelete is None:
        abort(404)
    storage.delete(todelete)
    storage.save()
    return jsonify({}), '200'
