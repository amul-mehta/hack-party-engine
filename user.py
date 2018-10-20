import datetime

def checkUser(user, db):
	users = db['user']
	return users.find_one({'username' : user['username']})


def createNewUser(user, db):
	users = db['user']
	user['created'] = datetime.datetime.utcnow()
	user['updated'] = datetime.datetime.utcnow()
	users.insert_one(user)

def login(details, db):
	users = db['user']
	user = users.find_one(
		{
		"username": details['username'],
		"password" : details['password']
		})

	return user

def update(user, db):
	users = db['user']
	users.update_one(
		{'username' : user['username']},
		{
			'$set' : {
				'password' : user['password'],
				'first_name' : user['first_name'],
				'last_name' : user['last_name'],
				'phone' : user['phone']
			},
			"$currentDate":{"updated":True}
		})