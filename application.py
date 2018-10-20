from flask import Flask, request, json, jsonify
from database import initializeDatabase
from user import *
from party import *
from restaurant import update_restaurant_for_user,get_restaurants_for_party_by_user

app = Flask(__name__)

db = initializeDatabase()

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
	if findUserByName(request.json["username"], db) == None:
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


@app.route("/api/user/update", methods=['POST'])
def updateUser():
	if (findUserByName(request.json["username"], db)) != None:
		update(request.json, db)
		return jsonify(message="User updated successfully")
	else:
		return jsonify(message="User could not be updated"), 400


@app.route("/api/party/create", methods=['POST'])
def createParty():
	if findUserByName(request.json["host_name"], db):
		create(request.json, db)
		return jsonify(message="party created successfully")
	else:
		return jsonify(message="User not found"), 404


@app.route("/api/party/find/<username>", methods=['GET'])
def findParties(username):
	return jsonify(getPartiesByUser(username, db))


@app.route("/api/party/response", methods=['POST'])
def partyResponse():
	response(request.json, db)
	return jsonify(message="response reported")


@app.route("/api/party/find/one/<partyId>", methods=['GET'])
def getParty(partyId):
	res = getPartyByPartyId(partyId, db)
	if res != None:
		res['_id'] = str(res['_id'])
		return jsonify(res)
	else:
		return jsonify(message="Party not found"), 404

@app.route('/api/restaurants/update', methods=['POST'])
def updateRestaurant():
	update_restaurant_for_user(
		db,request.json['restaurant_id'],
		request.json['user_id'], request.json['party_id']
	)
	return jsonify(message="Restaurant choice updated")

@app.route('/api/restaurants/<party_id>/<user_id>', methods = ['GET'])
def getRestaurantsByUserAndParty():
	return jsonify(get_restaurants_for_party_by_user(db,party_id,user_id))

def convertUser(data):
	return {
			'id' : str(data['_id']),
			'username' : data['username'],
			'first_name' : data['first_name'],
			'last_name' : data['last_name'],
			'phone' : data['phone'],
			'created' : data['created'],
			'updated' : data['updated'],
			'device_token' :  data.get('device_token', '')
		}


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
