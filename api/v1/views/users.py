#!/usr/bin/python3
"""
Init.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def ausers():
    """Users endpoint."""
    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'email' not in request.get_json():
            abort(400, "Missing email")
        if 'password' not in request.get_json():
            abort(400, "Missing password")
        u = User(**request.get_json())
        u.save()
        return jsonify(u.to_dict()), 201

    if request.method == 'GET':
        return jsonify([user.to_dict()
                        for user in storage.all('User').values()])


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user(user_id):
    """Users endpoint."""
    u = storage.get('User', user_id)

    if not user:
        abort(404)

    if request.method == 'GET':
        return jsonify(u.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(u)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, val in request.get_json().items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(u, key, val)
        u.save()
        return jsonify(u.to_dict()), 200
