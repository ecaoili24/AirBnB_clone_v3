#!/usr/bin/python3
""" view for review object that handles restful api """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.state import State
from models.review import Review
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_all(place_id):
    """Gets the list of all Review objects of a Place"""
    review_l = []  # review list
    reviews_all = storage.all('Review')
    get_place = storage.get("Place", place_id)
    if get_place is None:
        abort(404)
    for rev in reviews_all.values():  # rev = review items
        if item.place_id == place_id:
            review_l.append(rev.to_dict())
    return jsonify(review_l)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def review_retrieval(review_id):
    """Retrieves review object with matching review_id """
    rev = storage.get("Review", review_id)
    if rev is None:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review(review_id):
    """Delete a review"""
    rev = storage.get("Review", review_id)
    if rev is None:
        abort(404)
    rev.delete()
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def update_review(place_id):
    """Posts a state object from request"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    user_id = body.get('user_id')
    if not user_id:
        abort(400, "Missing user_id")
    text = body.get('text')
    if not text:
        abort(400, "Missing text")
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    new_rev = Review(**post_content)
    new_rev.place_id = place_id
    storage.new(new_rev)
    new_rev.save()
    storage.close()
    return jsonify(new_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def PUT_review(review_id):
    """Updates Review object"""
    rev = storage.get("Review", review_id)
    if rev is None:
        abort(404)
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "place_id", "user_id", "created_at", "updated_at"]
    for key, v in update_content.items():
        if key not in ignore_keys:
            setattr(review, key, v)
    rev.save()
    storage.close()
    return jsonify(rev.to_dict()), 200
