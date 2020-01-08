import bson
from bson import json_util, ObjectId
from bson.json_util import dumps
from flask import Flask, jsonify, request, json

from pymongo import MongoClient, mongo_client
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/language_db"
app.config['MONGO_DBNAME'] = 'language'
mongo = PyMongo(app)
client = MongoClient()
db = client['language']
collection = db['database']


@app.route("/my_api/all", methods=["GET"])
def show_all():
    output = []
    all_elements = collection.find()
    for data in all_elements:
        output.append(json.loads(json_util.dumps(data)))
    return jsonify(output)


@app.route("/my_api/all/<language>", methods=["GET"])
def show_all_desired_language(language):
    output = []
    all_elements = collection.find({}, {"_id": 0, "button_id": 1, language: 1})
    for data in all_elements:
        output.append(json.loads(json_util.dumps(data)))
    return jsonify(output)


@app.route("/my_api/get/<button_id>", methods=["GET"])
def get_button(button_id):
    lng = collection.find_one({"button_id": button_id})
    return dumps(lng)


@app.route("/my_api/delete/<button_id>", methods=["DELETE", "GET"])
def delete_button(button_id):
    lng = collection.find_one({"button_id": button_id})
    collection.remove(lng)
    return "Button has been removed"


@app.route("/my_api/add", methods=["POST"])
def add_button():
    user_json = request.json
    collection.insert_one(user_json)
    return "Added successfully"


@app.route("/my_api/get/<button_id>/<language>", methods=["PUT", "GET"])
def update_language_button(button_id, language):
    json_update = request.json[language]
    x = collection.find_one_and_update({"button_id": button_id}, {"$set": {language: json_update}}, upsert=True,
                                       return_document=True)
    return "Your button has been updated"


@app.route("/my_api/<language>/<button_id>", methods=["GET"])
def get_specific_buttons_value(language, button_id):
    x = collection.find({"button_id": button_id}, {"_id": 0, "button_id": 1, language: 1})
    return dumps(x)


if __name__ == "__main__":
    app.run(debug=True)
