#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles
all default RESTful API actions
"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities(state_id=None):
    """List retrieval of all Amenity objects of a State"""
    a_all = storage.all('Amenity')  # a_all = all Amenity objects
    amentityLIST = []
    for a_all in a_all.values():
        amentityLIST.append(a_all.to_dict())
    return jsonify(amentityLIST), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_retrieval(amenity_id=None):
    """Retrieval of Amenity objects with linked amenity ids"""
    amenity_dict = storage.all('Amenity')
    amenity = amenity_dict.get('Amenity' + "." + amenity_id)
    if amenity is None:  # if amenity_id is not linked to any Amenity obj
        abort(404)  # then, raise 404 error
    else:
        return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Deletes an Amenity object"""
    objects = storage.get('Amenity', amenity_id)
    if objects is None:
        abort(404)  # if the amenity_id is not linked to any Amenity object
    else:
        storage.delete(objects)
        storage.save()
    return jsonify({}), 200  # returns an empty dict with status code 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create an Amenity, from data provided by the request"""
    body = request.get_json()  # transfrom the HTTP body request to dict
    if not body:  # if HTTP body req is  not a valid JSON
        abort(400, {"Not a JSON"})  # raise err and message
    if 'name' not in body:  # if dict doesn't contain the key name
        abort(400, {"Missing name"})
    objects = Amenity(name=body['name'])
    storage.new(objects)
    storage.save()
    return jsonify(objects.to_dict()), 201  # returns new Amenity


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """Updating an existing Amenity object"""
    body = request.get_json()
    if not body:
        abort(400, {"Not a JSON"})
    objects = storage.get('Amenity', amenity_id)
    if objects is None:  # if amenity_id is not linked to any Amenity object
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']  # ignore keys
    for key, value in body.items():  # update Amenity obj with key-val pairs
        if key not in ignore_keys:
            setattr(objects, key, value)
    storage.save()
    return jsonify(objects.to_dict()), 200  # return Amenity obj
