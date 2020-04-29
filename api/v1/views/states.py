#!/usr/bin/python3
"""
A script that starts a Flask web application.
Create a new view for State objects that handles
all default RESTful API actions
"""

import os
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.state import City
from models.city import City

app = Flask(__name__)
app.url_map.strict_slashes = False


@app_views.route('/states', methods=['GET'])
def states_get():
    """List retrieival of all State objects"""
    states = storage.all('State')
    statesLIST = []
    for obj in states.values():
        statesLIST.append(obj.to_dict())
    return jsonify(statesLIST), 200


@app_views.route('/states/<state_id>', methods=['GET'])
def state_id_get(state_id=None):
    """List retrieval of given State object"""
    states = storage.all('State')
    state = states.get('State' + "." + state_id)
    if state is None:
        abort(404) # state_id is not linked to any State object, raise 404 error
    statesLIST = []
    return jsonify(state), 200


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state_id(state_id=None):
    """Deletes a state object"""
    objects = storage.get('State', state_id)
    if objects is None:
        abort(404)
    else:
        storage.delete(objects)
        storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def post_states():
    """Posts a state object from request"""
    state_dict = storage.all('State')
    if state_dict is None: #place_holder variable
        abort(404)
    body = request.get_json()
    if body is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in body:
        return jsonify({"error": "Missing name"}), 400
    storage.new(objects)
    storage.save()
    return jsonify(), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state_id(state_id=None):
    return("test5")
