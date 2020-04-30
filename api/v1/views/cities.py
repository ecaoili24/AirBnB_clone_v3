#!/usr/bin/python3
"""
A script that starts a Flask web application.
Create a new view for City objects that handles
all default RESTful API actions:
"""

import os
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.state import City
from models.city import City

app = Flask(__name__)


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id=None):
    """List retrieval of all City objects of a State"""
    states = storage.all('State')
    state = states.get('State' + "." + state_id)
    if state is None:
        abort(404)  # state_id is not linked to any State object, raise 404 err
    cityLIST = []
    cities = storage.all('City')
    for city in cities.values():
        if city.state_id == state_id:
            cityLIST.append(city.to_dict())  # serializes an obj to valid JSON
    return jsonify(cityLIST), 200  # return empty list with status code 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_retrieval(city_id=None):
    """Retrieval of City objects with linked ids"""
    city_dict = storage.all('City')
    city = city_dict.get('City' + "." + city_id)
    if city is None:  # if state_id is not linked to any State obj
        abort(404)
    else:
        return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """Deletes a City object"""
    objects = storage.get('City', city_id)
    if objects is None:
        abort(404)  # if the city_id is not linked to any City object
    else:
        storage.delete(objects)
        storage.save()
    return jsonify({}), 200  # returns an empty dict with status code 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id=None):
    """Create a City, from data provided by the request"""
    state_dict = storage.all('State')
    state = state_dict.get('State' + "." + state_id)
    if state is None:
        abort(404)
    body = request.get_json()  # transfrom the HTTP body request to dict
    if body is None:  # if HTTP body req is  not a valid JSON
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in body:  # if dict doesn't contain the key name
        return jsonify({"error": "Missing name"}), 400
    objects = City(name=body['name'], state_id=state_id)
    storage.new(objects)
    storage.save()
    return jsonify(objects.to_dict()), 201  # returns new City


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """Updating an existing City object"""
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    body = request.get_json()
    if body is None:
        return jsonify({"error": "Not a JSON"}), 400
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore_keys:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
