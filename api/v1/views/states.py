#!/usr/bin/python3
"""
Create a new view for State objects that handles
all default RESTful API actions
"""
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State

app = Flask(__name__)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """List retrieival of all State objects"""
    states = storage.all('State')
    statesLIST = []
    for obj in states.values():
        statesLIST.append(obj.to_dict())
    return jsonify(statesLIST), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id_get(state_id):
    """List retrieval of given State object"""
    states = storage.all('State')
    statesLIST = []
    for obj in states.values():
        if obj.id == state_id:
            statesLIST.append(obj.to_dict())
    if statesLIST is None or not statesLIST:
        abort(404)
    return jsonify(statesLIST), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state_id(state_id):
    """Deletes a state object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    """Posts a state object from request"""
    body = request.get_json(silent=True)
    if body is None:
        abort(400, "Not a JSON")
    if 'name' not in body:
        abort(400, "Missing name")
    NEWstate = State(**body)
    storage.new(NEWstate)
    storage.save()
    return jsonify(NEWstate.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state_id(state_id):
    """Updates the state object"""
    body = request.get_json(silent=True)
    if body is None:
        abort(400, "Not a JSON")
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
