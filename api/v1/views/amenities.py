#!/usr/bin/python3
"""
Init.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def aamenities():
    """Amenities endpoint."""
    if request.method == 'GET':
        return jsonify([a.to_dict()
                        for a in storage.all('Amenity').values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        a = Amenity(**request.get_json())
        a.save()
        return jsonify(a.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity(amenity_id):
    """Amenities endpoint."""
    a = storage.get('Amenity', amenity_id)
    if not a:
        abort(404)

    if request.method == 'GET':
        return jsonify(a.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(a)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, val in request.json.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(a, key, val)
        a.save()
        return jsonify(a.to_dict()), 200
