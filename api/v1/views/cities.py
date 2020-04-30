#!/usr/bin/python3
"""
Create a new view for City objects that handles
all default RESTful API actions:
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """List retrieval of all City objects of a State"""
    s = storage.get('State', state_id)  # s = states
    if s is None:
        abort(404)
    cities_all = s.cities_all
    c_list = []
    for c in cities_all:
        c_list.append(c.to_dict())
    return jsonify(c_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_retrieval(city_id):
    """Retrieval of City objects with linked ids"""
    city = storage.get('City', city_id)
    if city is None:  # if state_id is not linked to any State obj
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    bye_city = storage.get('City', city_id)
    if bye_city is None:
        abort(404)  # if the city_id is not linked to any City object
    bye_city.delete()
    storage.save()
    storage.reload()
    return jsonify({}), 200  # returns an empty dict with status code 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a City, from data provided by the request"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    body = request.get_json(silent=True)  # transfrom the HTTP body req to dict
    if body is None:  # if HTTP body req is  not a valid JSON
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in body:  # if dict doesn't contain the key name
        return jsonify({"error": "Missing name"}), 400
    name = request.get_json().get('name')
    city_new = City(name=name, state_id=state_id)
    city_new.save()
    return jsonify(city_new.to_dict()), 201  # returns new City


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updating an existing City object"""
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
