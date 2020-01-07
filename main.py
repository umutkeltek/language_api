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


@app.route("/all", methods=["GET"])
def show_all():
    output = []
    all_elements = collection.find()
    for data in all_elements:
        output.append(json.loads(json_util.dumps(data)))
    return jsonify(output)


@app.route("/get/<_id>", methods=["GET"])
def get_button(_id):
    lng = collection.find_one({"_id": ObjectId(bson.ObjectId(oid=str(_id)))})
    return dumps(lng)


@app.route("/delete/<_id>", methods=["DELETE"])
def delete_button(_id):
    lng = collection.find_one({"_id": ObjectId(bson.ObjectId(oid=str(_id)))})
    collection.remove(lng)
    print("Button has been removed")


@app.route("/add", methods=["POST"])
def add_button():
    user_json = request.json
    collection.insert_one(user_json)
    return "Added successfully"


@app.route("/get/<_id>/<language>", methods=["PUT","GET"])
def add_field(_id,language):
    x = collection.find_one({"_id": ObjectId(bson.ObjectId(oid=str(_id)))})
    collection.updateOne({"_id": ObjectId(bson.ObjectId(oid=str(_id))),},
        {"$set" : {language: "Gray"}})
   # collection.updateOne({x, "language": },{ $set: {"language.$"}})
    return "Updated successfully"


if __name__ == "__main__":
    app.run(debug=True)
