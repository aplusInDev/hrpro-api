#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Company, Job
from api.v1.auth.middleware import session_required


@app_views.route('/companies/<company_id>/jobs', methods=['GET'], strict_slashes=False)
def get_jobs(company_id):
    """ get jobs """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)

    all_jobs = [job.to_dict() for job in company.jobs]
    return jsonify(all_jobs)

@app_views.route('/jobs/<job_id>', methods=['GET'], strict_slashes=False)
def get_job(job_id):
    """ get job """
    job = storage.get(Job, job_id)
    if job is None:
        abort(404)
    return jsonify(job.to_dict())

@app_views.route('/companies/<company_id>/jobs', methods=['POST'], strict_slashes=False)
@session_required
def post_job(account, company_id):
    """ post job """
    if account.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    data = request.form
    if not data:
        return jsonify({"error": "unvalid request"}), 400
    else:
        data = data.to_dict()
    from api.v1.utils.validate_field import handle_update_info
    data = handle_update_info("job", company_id, data)
    if data:
        data = str(data)
        new_job = Job(info=data, company_id=company_id)
        new_job.save()
        return jsonify(new_job.to_dict()), 201
    return jsonify({"error": "unvalid request"}), 400

@app_views.route('/jobs/<job_id>', methods=['PUT'], strict_slashes=False)
@session_required
def put_job(account, job_id):
    """ put job """
    if account.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    job = storage.get(Job, job_id)
    if job is None:
        abort(404)
    data = request.form
    if not data:
        return jsonify({"error": "unvalid request"}), 400
    else:
        data = data.to_dict()
    from api.v1.utils.validate_field import handle_update_info
    data = handle_update_info("job", job.company_id, data)
    if data:
        job.info = str(data)
        job.save()
        return jsonify(job.to_dict())
    return jsonify({"error": "unvalid request"}), 400

@app_views.route('/jobs/<job_id>', methods=['DELETE'], strict_slashes=False)
def delete_job(job_id):
    """ delete job """
    job = storage.get(Job, job_id)
    if job is None:
        abort(404)
    job.delete()
    return jsonify({}), 200
