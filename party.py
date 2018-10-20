import datetime
from bson.objectid import ObjectId
from restaurant import initialize_restaurants
from notification import send_notifications_to_attendes


def create(party, db):
	parties = db['party']

	party['created'] = datetime.datetime.utcnow()
	party['updated'] = datetime.datetime.utcnow()
	createdParty = parties.insert_one(party)

	party['attendees'][party['host_name']] = True
	party['_id'] = createdParty.inserted_id

	addUserParties(party, createdParty.inserted_id, db)
	initialize_restaurants(db, party)
	send_notifications_to_attendes(db, party)


def getPartiesByUser(username, db):
	res = []
	parties = db['party']
	userParties = db['user_parties']

	userParties = userParties.find_one({'username' : username})

	if userParties:
		for up in userParties["parties"]:
			party = parties.find_one({'_id' : ObjectId(up)})
			party["_id"] = str(party["_id"])
			if party['host_name'] == username:
				party['attending'] = True
			else:
				party['attending'] = party['attendees'][username]

			res.append(party)

	return res


def getPartyByPartyId(partyId, db):
	parties = db['party']
	return parties.find_one({'_id' : ObjectId(partyId)})

def response(response, db):
	parties = db['party']
	userParties = db['user_parties']

	parties.update_one(
		{'_id' : ObjectId(response['partyId'])},
		{
			'$set' : {
				'attendees.{}'.format(response['responder']) : response['response']
			},
			"$currentDate":{"updated":True}
		})

	if response['response'] == False:
		userParties.update_one(
    			{ "username" : response['responder']},
			    { '$pull': { 'parties': { '$in' : [response['partyId']] }}
			    })



def addUserParties(party, partyId, db):
	userParties = db['user_parties']

	for username in party['attendees'].keys():
		if userParties.find_one({'username' : username}) == None:
			rel = {
				"username"  : username,
				"parties" : [str(partyId)]
			}

			userParties.insert_one(rel)
		else:
			userParties.update({'username': username}, {'$push': {'parties': str(partyId)}})

