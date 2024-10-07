from flask import Blueprint, jsonify, request
from database.__init__ import database
from models.user_model import User
from controllers.user_controller import create_user


user = Blueprint("user", __name__)


@user.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in database['SCHOOL_PY_PROJECT']['Users'].find():
        user['_id'] = str(user['_id'])
        users.append(user)
    return jsonify(users)


@user.route('/users', methods=['POST'])
def add_user():

    my_body = request.json

    my_user = User(my_body["name"], my_body["email"], my_body["password"])

    result = create_user(my_user)

    return jsonify({"id": str(result.inserted_id)})
