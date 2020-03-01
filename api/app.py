from pymongo import MongoClient
from flask import Flask, jsonify, request
from bson.json_util import dumps

client = MongoClient('mongodb://JeanM:jeanm@127.0.0.1:27017/tot')
db_tot = client.tot
userCollection = db_tot.Users

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

app = Flask(__name__)

@app.route('/api/v1/users/all', methods=["GET"])
def allUsers():
    cursor = userCollection.find({}, {'_id': False})
    return dumps(cursor)

@app.route('/api/v1/users/add', methods=["POST"])
def addUser():
    if request.json != None:
        userCollection.insert_one(request.json)
        return "200 - OK"
    else :
        raise InvalidUsage("Missing json data", status_code=410)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)