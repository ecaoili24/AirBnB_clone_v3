#!/usr/bin/python3
"""
Create a new view for State objects that handles
all default RESTful API actions
"""

from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State

app.url_map.strict_slashes = False


@app_views.route('/states', methods=['GET'])
def states_all():
    """List retrieival of all State objects"""
    states = storage.all('State')
    states_all = [v.to_dict() for key, value in states.items()]
    return jsonify(states_all)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_id_get(state_id):
    """List retrieval of given State object"""
    states = storage.all('State')
    state_name = ('State' + state_id)
    state = [v.to_dict() for key, value in states.items() if key == state_name
    if len(state) is not 1:
        abort(404)  # state_id not linked to any State obj, raise 404 error
    return jsonify(state[0])


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state_id(state_id):
    """Deletes a state object"""
    bye_state= storage.get('State', state_id)
    if not bye_state:
        abort(404)
    storage.delete(bye_state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def post_states():
    """Posts a state object from request"""
    body= request.get_json(silent=True)
    if body is None:  # place_holder variable
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    NEWstate= State(**body)
    storage.new(NEWstate)
    storage.save()
    return jsonify(NEWstate.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state_id(state_id):
    "Updates the state object"""
    body= request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    states_data= storage.all('State')
    state= None
    for S in states_data:
        if state_id in S:
             state= state[S]
    if not state:
        abort(404)
    ignore_keys= ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore_keys:
             setattr(state, key, value)
             storage.save()
    return jsonify(state.to_dict())
