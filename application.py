from flask import Flask, request, json, jsonify
from database import main

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/connect", methods=['GET'])
def connect():
	x = main()

	res = {
		'id' : str(x['_id']),
		'name' : x['name']
	}

	return jsonify(res)

@app.route("/api/create/user", methods=['POST'])
def createUser():
	print(request.data)
