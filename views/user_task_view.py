from flask import Blueprint, jsonify, request
from database.__init__ import database
from controllers.task_controller import create_task, fetch_tasks, fetch_assigned_to, update_task, delete_task
from models.task_model import Task
from helpers.token_validation import validate_jwt

task = Blueprint("tasks", __name__)

@task.route('/tasks', methods=['POST'])
def add_task():
    try:
        token = validate_jwt()
        my_body = request.json

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        if 'description' not in my_body:
            return jsonify({'error': 'Description is needed in the request!'}), 400
        if 'assignedToUid' not in my_body:
            return jsonify({'error': 'assignedToUid is needed in the request!'}), 400
        if 'assignedToName' not in my_body:
            return jsonify({'error': 'assignedToName is needed in the request!'}), 400
        if 'createdByUid' not in my_body:
            return jsonify({'error': 'createdByUid is needed in the request!'}), 400
        if 'createdByName' not in my_body:
            return jsonify({'error': 'createdByName is needed in the request!'}), 400
        if 'done' not in my_body:
            return jsonify({'error': 'done is needed in the request!'}), 400

        my_task = Task(my_body["createdByUid"], my_body["createdByName"], my_body["assignedToUid"], my_body["assignedToName"], my_body["description"], my_body["done"])

        result = create_task(my_task)

        if not result.inserted_id:
            return jsonify({'error': 'Something wrong happened when creating task!'}), 500

        return jsonify({"id": str(result.inserted_id)})
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


@task.route('/tasks/createdby', methods=['GET'])
def get_tasks():
    try:
        token = validate_jwt()
        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401
        
        return fetch_tasks(token=token)
    except:
        return jsonify({'error': 'Something wrong happened when fetching tasks!'}), 500
    
@task.route('/tasks/assignedto', methods=['GET'])
def get_assigned_to():
    try:
        token = validate_jwt()
        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401
        
        return fetch_assigned_to(token=token)
    except:
        return jsonify({'error': 'Something wrong happened when fetching tasks!'}), 500
    
@task.route('/tasks/<taskUid>', methods=['PATCH'])
def update_task_route(taskUid):
    try:
        token = validate_jwt()
        my_body = request.json

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        if 'done' not in my_body:
            return jsonify({"error": 'Status done not found in the request'}), 400

        result = update_task(taskUid, token, my_body['done'])

        print(f"Update result: {result}")

        if not result.modified_count :
            return jsonify({'message': 'Status is not updated!'}), 400

        return jsonify({"id": result.taskUid})
    except:
        return jsonify({'error': 'Something wrong happened when updating task!'}), 500
    
@task.route('/v1/tasks/<taskUid>', methods=['DELETE'])
def deleteTask(taskUid):
    try:
        token = validate_jwt()
        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401

        return delete_task(taskUid, token)
    except:
        return jsonify({'error': 'Something went wrong when deleting the task!'}), 500