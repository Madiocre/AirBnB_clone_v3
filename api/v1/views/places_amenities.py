#!/usr/bin/python3
"""
Init.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def allamen(place_id):
    """Amenities endpoint."""
    p = storage.get('Place', place_id)
    if not p:
        abort(404)
    if not p.amenities:
        return jsonify([])
    return jsonify([amen.to_dict() for amen in p.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def pamenity(place_id, amenity_id):
    """Amenities endpoint."""
    a = storage.get('Amenity', amenity_id)
    p = storage.get('Place', place_id)
    if not a or not p:
        abort(404)
    if request.method == 'DELETE':
        if a not in p.amenities:
            abort(404)
        storage.delete(a)
        storage.save()
        return jsonify({}), 200
    if request.method == 'POST':
        if a not in p.amenities:
            p.amenities.append(a)
            p.save()
            return jsonify(a.to_dict()), 201
        return jsonify(a.to_dict()), 200
