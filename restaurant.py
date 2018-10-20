from nearby_restaurants import get_nearby_restaurants
from bson.objectid import ObjectId


def initialize_restaurants(db, party):
	location = party['location']
	lat = location['lat']
	long = location['lng']
	
	res_list = get_nearby_restaurants(lat,long)
	r_list = []
	for r in res_list:
		r['party_id'] = party['_id']
		r_list.append(r)	
	collection = db['restaurants']
	
	collection.insert_many(r_list)

def update_restaurant_for_user(db, restaurant, user):
	pass


def get_restaurants_for_party_by_user(db, party_id, username):
	# TODO : Check this after initializing polls
	restaurants = db['restaurants']
	user_restaurants = db['user_restaurants']
	res = collection.find({'party_id' : ObjectId(party_id)})
	for r in res:
		r['_id'] = str(party['_id'])
		result.append(r)
	return result
	
	
