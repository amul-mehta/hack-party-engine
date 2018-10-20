import datetime

def checkUser(user, db):
	users = db['user']
	return users.find_one({'username' : user['username']})


def createNewUser(user, db):
	users = db['user']
	user['created'] = datetime.datetime.utcnow()
	users.insert_one(user)

def login(details, db):
	users = db['user']
	user = users.find_one(
		{
		"username": details['username'],
		"password" : details['password']
		})

	return user
