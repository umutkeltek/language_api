from bson import json_util
from flask import Flask, jsonify, request, json
from pymongo import MongoClient
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
    all_elements = collection.find({}, {"_id": 1, language: 1})
    for data in all_elements:
        output.append(json.loads(json_util.dumps(data)))
    return jsonify(output)


@app.route("/my_api/<_id>", methods=["GET"])
def get_button(_id):
    lng = collection.find_one({"_id": _id})
    return jsonify(json.loads(json_util.dumps(lng)))


@app.route("/my_api/delete/<_id>", methods=["DELETE", "GET"])
def delete_button(_id):
    lng = collection.find_one({"_id": _id})
    collection.remove(lng)
    return "Button has been removed"


@app.route("/my_api/add", methods=["POST"])
def add_button():
    field_name = request.json["_id"]
    user_json = request.json
    collection.insert_one(user_json, field_name)
    return "Added successfully"


@app.route("/my_api/update/<_id>/<language>", methods=["PUT", "GET"])
def update_language_button(_id, language):
    json_update = request.json[language]
    x = collection.find_one_and_update({"_id": _id}, {"$set": {language: json_update}}, upsert=True,
                                       return_document=True)
    return "Your button has been updated"


@app.route("/my_api/get/<language>/<_id>", methods=["GET"])
def get_specific_buttons_value(_id, language):
    x = collection.find({"_id": _id}, {_id: 1, language: 1})
    return jsonify(json.loads(json_util.dumps(x)))


@app.route("/my_api/update/<_id>", methods=["PUT", "GET"])
def update_all_language_field(_id):
    user_json = request.json
    x = collection.find_one_and_update({"_id": _id}, {"$set": user_json}, upsert=True,
                                       return_document=True)

    return "Your button has been updated"


if __name__ == "__main__":
    app.run(debug=True)
