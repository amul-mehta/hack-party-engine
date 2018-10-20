from flask import Flask, request, json, jsonify
from database import initializeDatabase
from user import *

app = Flask(__name__)

db = None

@app.route("/", methods=['GET'])
def hello():
	return "Hello World!"

@app.route("/connect", methods=['GET'])
def connect():

	collection = db['user']
	cols = collection.find()
	res = []

	for user in cols: 

		t = convertUser(user)

		res.append(t)


	return jsonify(res)

@app.route("/api/user/create", methods=['POST'])
def createUser():
	if checkUser(request.json, db) == None:
		createNewUser(request.json, db)
		return jsonify(message="User successfully created")
	else:
		return jsonify(message="User already exists"), 409


@app.route("/api/user/login", methods=['POST'])
def loginUser():
	res = login(request.json, db)
	if res != None:
		return jsonify(convertUser(res)), 200
	else:
		return jsonify(message="User not found"), 404


def convertUser(data):
		return {
			'id' : str(data['_id']),
			'username' : data['username'],
			'first_name' : data['first_name'],
			'last_name' : data['last_name'],
			'phone' : data['phone'],
			'created' : data['created']
		}


if __name__ == '__main__':
	db = initializeDatabase()
	app.run(host='0.0.0.0', debug=True)
