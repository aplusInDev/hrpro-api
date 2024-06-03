#!/usr/bin/env python3

""" evaluation view """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, Evaluation


@app_views.route('/employees/<employee_id>/evaluations', methods=['GET'], strict_slashes=False)
def get_employee_evaluations(employee_id):
    """ Retrieves the list of all evaluations of a employee """
    employee = storage.get("Employee", employee_id)
    if not employee:
        abort(404)
    evaluations = [evaluation.to_dict() for evaluation in employee.evaluations]
    return jsonify(evaluations)

@app_views.route('/trainings/<training_id>/evaluations', methods=['GET'])
def get_training_evaluations(training_id):
    """ Retrieves the list of all evaluations for training program """
    training = storage.get("Training", training_id)
    if not training:
        abort(404)
    evaluations = [evaluation.to_dict() for evaluation in training.evaluations]
    return jsonify(evaluations)

@app_views.route('/evaluations/<evaluation_id>', methods=['GET'])
def get_evaluation(evaluation_id):
    """ Retrieves a evaluation """
    evaluation = storage.get("Evaluation", evaluation_id)
    if not evaluation:
        abort(404)
    return jsonify(evaluation.to_dict())

@app_views.route('/evaluations/<evaluation_id>', methods=['DELETE'])
def delete_evaluation(evaluation_id):
    """ Deletes a evaluation """
    evaluation = storage.get("Evaluation", evaluation_id)
    if not evaluation:
        abort(404)
    storage.delete(evaluation)
    storage.save()
    return jsonify({}), 200

@app_views.route('/trainings', methods=['POST'])
def create_evaluation() -> dict:
    """ create new evaluation
    Args:
        trainee_id: the trainee id
        training_id: the evaluated training id
    Returns:
        new evaluation dict
    """
    trainee_id = request.args["trainee_id"]
    training_id = request.args["training_id"]
    if not trainee_id:
        return jsonify({"error": "trainee_id required"})
    if not training_id:
        return jsonify({"error": "training_id required"})
    evaluation = storage.found_evaluation_by(employee_id=trainee_id,
                                             training_id=training_id)
    if evaluation:
        return jsonify(
            {"message": "you have only one evaluation per training"})
    data = request.form.to_dict()
    required_fields = ["score", "anonimous"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"})
        
    evaluation = Evaluation(**data, training_id=training_id,
                            employee_id=trainee_id)
    evaluation.save()
    return jsonify(evaluation.to_dict())

@app_views.route('/check_evaluation_status', methods=["GET"])
def check_evaluation_status():
    """ check giving evaluation status """
    trainee_id = request.args["trainee_id"]
    training_id = request.args["training_id"]
    if not trainee_id:
        return jsonify({"error": "trainee_id required"}), 400
    if not training_id:
        return jsonify({"error": "training_id required"}), 400
    training = storage.get("Training", training_id)
    trainee = storage.get("Employee", trainee_id)
    if not training:
        return jsonify({"error": "training not found"}), 404
    if not trainee:
        return jsonify({"error": "trainee not found"}), 404
        
    evaluation = storage.found_evaluation_by(employee_id=trainee_id,
                                             training_id=training_id)
    if evaluation:
        return jsonify({
            "training": training.title,
            "is_evaluated": True
            })
    return jsonify({
        "training": training.title,
        "is_evaluated": False
    })