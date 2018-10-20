import datetime
from bson.objectid import ObjectId

def create(party, db):
	parties = db['party']

	party['created'] = datetime.datetime.utcnow()
	party['updated'] = datetime.datetime.utcnow()
	createdParty = parties.insert_one(party)

	party['attendees'].append(party['host_name'])

	addUserParties(party, createdParty.inserted_id, db)

def getPartiesByUser(username, db):
	res = []
	parties = db['party']
	userParties = db['user_parties']

	userParties = userParties.find_one({'username' : username})

	for up in userParties["parties"]:
		party = parties.find_one({'_id' : ObjectId(up)})
		party["_id"] = str(party["_id"])
		res.append(party)
		
	return res

def addUserParties(party, partyId, db):
	userParties = db['user_parties']

	for username in party['attendees']:
		if userParties.find_one({'username' : username}) == None:
			rel = {
				"username"  : username,
				"parties" : [str(partyId)]
			}

			userParties.insert_one(rel)
		else:
			userParties.update({'username': username}, {'$push': {'parties': str(partyId)}})

