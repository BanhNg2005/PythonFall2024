from flask import Flask, jsonify, request
from pymongo import MongoClient
from views.user_view import user

app = Flask(__name__)

app.register_blueprint(user)

@app.route('/', methods=['GET'])
def home():
    return "<h1>HOME</h1>"

if __name__ == '__main__':
    app.run()
