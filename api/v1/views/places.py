#!/usr/bin/python3
"""
Init.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """Places endpoint."""
    c = storage.get('City', city_id)
    if not c:
        abort(404)

    if request.method == 'GET':
        return jsonify([p.to_dict() for p in c.places])

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'user_id' not in request.get_json():
            abort(400, 'Missing user_id')
        if not storage.get('User', request.get_json()['user_id']):
            abort(404)
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        p = Place(**request.get_json())
        p.city_id = city_id
        p.save()
        return jsonify(p.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place(place_id):
    """Places endpoint."""
    p = storage.get('Place', place_id)
    if not p:
        abort(404)

    if request.method == 'GET':
        return jsonify(p.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(p)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, "Not a JSON")
        for key, val in request.get_json().items():
            if key not in ["user_id", "city_id",
                           "id", "created_at", "updated_at"]:
                setattr(p, key, val)
        p.save()
        return jsonify(p.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Places endpoint."""
    headers = request.headers.get('Content-Type')
    if headers != 'application/json':
        abort(400, 'Not a JSON')

    if not request.get_json():
        return jsonify([p.to_dict() for
                        p in storage.all('Place').values()])

    res = []
    p = []
    a = []
    obj = request.get_json()

    for k, v in obj.items():
        if k == 'states':
            for item in v:
                state_obj = storage.get('State', item)
                for city in state_obj.cities:
                    res.append(city.id)
    for k, v in obj.items():
        if k == 'cities':
            for item in v:
                if item not in res:
                    res.append(item)

    for k, v in obj.items():
        if k == 'amenities':
            for item in v:
                if item not in res:
                    a.append(item)

    for place in storage.all('Place').values():
        if place.city_id in res:
            p.append(place.id)

    if p == [] and a != []:
        remove = []
        res = []
        p = [place.id for place in storage.all('Place').values()]
        for place in p:
            obj = storage.get('Place', place)
            for amen in obj.amenities:
                if amen.id not in a:
                    if place not in remove:
                        remove.append(place)
        for place in p:
            if place not in remove:
                res.append(place)
        return jsonify([storage.get('Place', obj).to_dict()
                        for obj in res])

    if a != []:
        for place in p:
            obj = storage.get('Place', place)
            for amenity in a:
                if amenity not in obj.amenities:
                    p.remove(place)

    return jsonify([storage.get('Place', id).to_dict() for id in p])
