#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Company, Job


@app_views.route('/companies/<company_id>/jobs', methods=['GET'], strict_slashes=False)
def get_jobs(company_id):
    """ get jobs """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    return jsonify([job.to_dict() for job in company.jobs])

@app_views.route('/companies/<company_id>/jobs_titles', methods=['GET'])
def get_jobs_names(company_id):
    """ get the list of company jobs titles """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    all_jobs = []
    for job in company.jobs:
        all_jobs.append(job.title)
    return jsonify(all_jobs), 200

@app_views.route('/jobs/<job_id>', methods=['GET'], strict_slashes=False)
def get_job(job_id):
    """ get job """
    job = storage.get(Job, job_id)
    if job is None:
        abort(404)
    return jsonify(job.to_dict())

@app_views.route('/companies/<company_id>/jobs', methods=['POST'], strict_slashes=False)
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
    if not data:
        return jsonify({"error": "unvalid request"}), 400
    job_title = data.get("title")
    data = str(data)
    new_job = Job(title=job_title, info=data, company_id=company_id)
    new_job.save()
    return jsonify(new_job.to_dict()), 201

@app_views.route('/jobs/<job_id>', methods=['PUT'], strict_slashes=False)
def put_job(account, job_id):
    """ put job """
    if account.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401
    job = storage.get(Job, job_id)
    if job is None:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a json data"}), 400

    from api.v1.utils.validate_field import handle_update_info
    data = handle_update_info("job", job.company_id, data)
    if not data:
        return jsonify({"error": "unvalid request"}), 400
    if "title" in data:
        job.title = data["title"]
    job.info = str(data)
    job.save()
    return jsonify(job.to_dict())

@app_views.route('/jobs/<job_id>', methods=['DELETE'], strict_slashes=False)
def delete_job(job_id):
    """ delete job """
    job = storage.get(Job, job_id)
    if job is None:
        abort(404)
    job.delete()
    return jsonify({}), 200
