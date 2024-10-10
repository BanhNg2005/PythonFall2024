from flask import Blueprint, jsonify, request
from database.__init__ import database
from models.user_model import User
from controllers.user_controller import create_user, login_user


user = Blueprint("user", __name__)

@user.route('/v0/users/signup', methods=['POST'])
def add_user():
    try: 
        my_body = request.json

        if 'email' not in my_body:
            return jsonify({'error': 'Email is needed in the request!'}), 400
        if 'name' not in my_body:
            return jsonify({'error': 'Name is needed in the request!'}), 400
        if 'password' not in my_body:
            return jsonify({'error': 'Password is needed in the request!'}), 400

        my_user = User(my_body["name"], my_body["email"], my_body["password"])

        result = create_user(my_user)

        if result == "Duplicated User":
            return jsonify({'error': 'There is already an user with this email!'}), 400
        
        if not result.inserted_id:
            return jsonify({'error': 'Something wrong happened when creating user!'}), 500

        return jsonify({"id": str(result.inserted_id)})
    except:
        return jsonify({'error': 'Something wrong happened when creating user!'}), 500

@user.route('/v0/users/login', methods=['POST'])
def login():
    my_body = request.json

    if 'email' not in my_body:
        return jsonify({'error': 'Email is needed in the request!'}), 400
    if 'password' not in my_body:
        return jsonify({'error': 'Password is needed in the request!'}), 400

    return login_user(my_body)


@user.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in database['SCHOOL_PY_PROJECT']['Users'].find():
        user['_id'] = str(user['_id'])
        users.append(user)
    return jsonify(users)


