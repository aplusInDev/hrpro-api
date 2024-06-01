#!/usr/bin/env python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Training


@app_views.route('/companies/<company_id>/trainings', methods=['GET'], strict_slashes=False)
def get_company_trainings(company_id):
    """ get company trainings view
    return all trainings for a company
    Args:
        company_id: the id of
    """
    company = storage.get("Company", company_id)
    if not company:
        return jsonify({"error": "company not found"}), 404
    return jsonify([training.to_dict() for training in company.trainings])

@app_views.route('/departments/<department_id>/trainings', methods=['GET'], strict_slashes=False)
def get_department_trainings(department_id):
    """ get department trainings view
    return all trainings for a department
    Args:
        department_id: the id of
    """
    department = storage.get("Department", department_id)
    if not department:
        return jsonify({"error": "department not found"}), 404
    return jsonify([training.to_dict() for training in department.trainings])

@app_views.route('/jobs/<job_id>/trainings', methods=['GET'], strict_slashes=False)
def get_job_trainings(job_id):
    """ get job trainings view
    return all trainings for a job
    Args:
        job_id: the id of
    """
    job = storage.get("Job", job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404
    return jsonify([training.to_dict() for training in job.trainings])

@app_views.route('/trainings/<training_id>', methods=['GET'], strict_slashes=False)
def get_training(training_id):
    """ get training view
    return a training
    Args:
        training_id: the id of the training
    """
    training = storage.get("Training", training_id)
    if not training:
        return jsonify({"error": "training not found"}), 404
    return jsonify(training.to_dict())

@app_views.route('/companies/<company_id>/trainings', methods=['POST'], strict_slashes=False)
def create_training(company_id):
    """ create training view
    create a new training
    Args:
        title: the title of the training
        description: the description of the training
        start_date: the start date of the training
        end_date: the end date of the training
        company_id: the id of the company
        department_id: the id of the department
        job_id: the id of the job
        trainer_id: the id of the trainer
    """
    company = storage.get("Company", company_id)
    if not company:
        return jsonify({"error": "company not found"}), 404
    required_fileds = ['title', 'start_date', 'end_date']
    data = request.form.to_dict()
    for field in required_fileds:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    if "department" in data:
        department = storage.find_department_by(name=data["department"])
        if department:
            data["department_id"] = department.id
            del data["department"]
        else:
            return jsonify({"error": "department not found"}), 404
    if "job" in data:
        job = storage.find_job_by(title=data["job"])
        if job:
            data["job_id"] = job.id
            del data["job"]
        else:
            return jsonify({"error": "job not found"}), 404
    if "trainer" in data:
        first_name = data["trainer"].split(" ")[0]
        last_name = data["trainer"].split(" ")[1]
        trainer = storage.find_employee_by(first_name=first_name, last_name=last_name)
        if trainer:
            data["trainer_id"] = trainer.id
            del data["trainer"]
        else:
            return jsonify({"error": "trainer not found"}), 404
    training = Training(**data, company_id=company_id)
    training.save()
    return jsonify(training.to_dict()), 201

@app_views.route('/trainings/<training_id>/trainees', methods=['POST'], strict_slashes=False)
def add_trainees(training_id):
    """ add trainees view
    add trainees to a training
    Args:
        training_id: the id of the training
        trainees: the ids of the trainees
    """
    training = storage.get("Training", training_id)
    if not training:
        return jsonify({"error": "training not found"}), 404
    data = request.form.to_dict()
    if "trainees" not in data:
        return jsonify({"error": "trainees is required"}), 400
    trainees = eval(data['trainees'])
    for trainee_full_name in trainees:
        first_name = trainee_full_name.split(" ")[0]
        last_name = trainee_full_name.split(" ")[1]
        trainee = storage.find_employee_by(
            first_name=first_name, last_name=last_name,
            company_id=training.company_id
        )
        if not trainee:
            return jsonify({"error": f"trainee {trainee_full_name} not found"}), 404
        training.trainees.append(trainee)
    training.save()
    return jsonify(training.to_dict())
