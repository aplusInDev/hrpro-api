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
def post_job(company_id):
    """ post job """
    company = storage.get(Company, company_id)
    if company is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'info' not in data:
        return 'Job Informations missing', 400
    job = Job(**data)
    job.company_id = company_id
    job.save()
    return jsonify(job.to_dict()), 201

@app_views.route('/jobs/<job_id>', methods=['PUT'], strict_slashes=False)
def put_job(job_id):
    """ put job """
    job = storage.get(Job, job_id)
    if job is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(job, key, value)
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
