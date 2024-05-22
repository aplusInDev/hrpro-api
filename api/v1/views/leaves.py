#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Leave
from api.v1.auth.middleware import requires_auth


@app_views.route('/leaves', methods=['GET'], strict_slashes=False)
@requires_auth(["admin", "hr"])
def get_leaves():
    """ get leaves view
    return all leaves for each employee in the company
    based on the giving year
    Args:
        company_id: the id of the company
        year: the year of the leaves
    """
    required_args = ['company_id', 'year']
    for arg in required_args:
        if arg not in request.args.to_dict():
            return jsonify({"error": f"{arg} is required"}), 400
    company_id = request.args.get("company_id")
    year = request.args.get("year")
    leaves = storage.get_leaves(company_id, year)
    return jsonify(leaves)
