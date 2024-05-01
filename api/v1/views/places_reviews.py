#!/usr/bin/python3
"""
Init.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviewinplace(place_id):
    """Reviews endpoint."""
    p = storage.get('Place', place_id)
    if p is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([review.to_dict()
                        for review in p.reviews])

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'user_id' not in request.get_json():
            abort(400, 'Missing user_id')
        if 'text' not in request.get_json():
            abort(400, 'Missing text')
        if not storage.get('User', request.get_json()['user_id']):
            abort(404)
        r = Review(**request.get_json())
        r.place_id = place_id
        r.save()
        return jsonify(r.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review(review_id):
    """Reviews endpoint."""
    r = storage.get('Review', review_id)
    if r is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(r.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(r)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, "Not a JSON")
        for key, value in request.get_json().items():
            if key not in ["id", "user_id", "place_id",
                           "created_at", "updated_at"]:
                setattr(r, key, value)
        r.save()
        return jsonify(r.to_dict()), 200
