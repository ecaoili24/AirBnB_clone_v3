#!/usr/bin/python3
"""
Create a new view for Places objects that handles
all default RESTful API actions
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """List retrieval of all Place objects for a city"""
    cities_all = storage.all('City', city_id)
    if city_all is None:
        abort(404)
    placesLIST = []
    places_all = storage.all('Place').values()
    city_p = [p.to_dict() for p in places_all if p.city_id == city_id]
    return jsonify(city_p)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_retrieval(place_id=None):
    """Retrieval of Place objects with linked place ids"""
    place = storage.get('Place', place_id)
    if place is None:  # if place_id is not linked to any place obj
        abort(404)  # then, raise 404 error
    else:
        return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a Place object"""
    objects = storage.get('Place', place_id)
    if objects is None:
        abort(404)  # if the user_id is not linked to any User object
    storage.delete(objects)
    storage.save()
    return jsonify({}), 200  # returns an empty dict with status code 200


@app_views.route('/cities/<city_id>/place', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id=None):
    """Create a Place, from data provided by the request"""
    city_object = storage.get('City', city_id)
    if city_object is None:  # if the city_id is not linked to any City obj
        abort(404)  # raise a 404 error
    body = request.get_json()  # Flask to transform HTTP request to a dict
    if body is None:  # If the HTTP request body is not valid JSON
        abort(400, {"error": "Not a JSON"})  # raise err and message
    if 'user_id' not in body:  # If the dict doesn't contain the key user_id
        abort(400, {"Missing user_id"})  # raise err
    user_object = storage.get('User', body['user_id'])
    if user_object is not None:  # user_id is not linked to any User object
        abort(404)  # raise err
    if 'name' not in body:  # If the dict doesn't contain the key name
        abort(400, {"Missing name"})
    place_object = Place(city_id=city_id)
    for key, value in body.items():
        setattr(place_object, key, value)
    storage.new(place_object)
    storage.save()
    return jsonify(place_object.to_dict()), 201  # returns new Place


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id=None):
    """Updating an existing Place object"""
    place_object = storage.get('Place', place_id)
    if place_object is None:
        abort(404)
    body = request.get_json()
    if body is None:
        abort(400, {"Not a JSON"})
    ignore_keys = ['id', 'city_id', 'user_id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore_keys:
            setattr(place_object, key, value)
    storage.save()
    return jsonify(place_object.to_dict()), 200  # return Place obj
