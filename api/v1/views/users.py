#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles
all default RESTful API actions
"""
import os
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users(state_id):
    """List retrieval of all User objects of a State"""
    users_all = storage.all('User')
    usersLIST = []
    for users_all in users_all.values():
        usersLIST.append(user_all.to_dict())
    return jsonify(usersLIST), 200


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_retrieval(user_id):
    """Retrieval of User objects with linked amenity ids"""
    user_dict = storage.all('User')
    user = user_dict.get('User' + "." + user_id)
    if user is None:  # if user_id is not linked to any user obj
        abort(404)  # then, raise 404 error
    else:
        return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    objects = storage.get('User', user_id)
    if objects is None:
        abort(404)  # if the user_id is not linked to any User object
    else:
        storage.delete(objects)
        storage.save()
    return jsonify({}), 200  # returns an empty dict with status code 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a User, from data provided by the request"""
    body = request.get_json()  # transfrom the HTTP body request to dict
    if not body:  # if HTTP body req is  not a valid JSON
        abort(400, {"Not a JSON"})  # raise 400 err with the message Not a JSON
    if 'email' not in body:  # if the dict doesn't contain the key email
        abort(400, {"Missing email"})  # raise err and message
    if 'password' not in body:  # if the dict doesn't contain the key passwd
        abort(400, {"Missing password"})  # raise err and message
    objects = User()
    for key, value in body.items():
        setattr(objects, key, value)
    storage.new(objects)
    storage.save()
    return jsonify(objects.to_dict()), 201  # returns new User


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updating an existing Amenity object"""
    body = request.get_json()
    if not body:
        abort(400, {"Not a JSON"})
    objects = storage.get('User', user_id)
    if objects is None:  # if user_id is not linked to any User object
        abort(404)
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']  # ignore keys
    for key, value in body.items():  # update User obj with key-val pairs
        if key not in ignore_keys:
            setattr(objects, key, value)
    storage.save()
    return jsonify(objects.to_dict()), 200  # return User obj
