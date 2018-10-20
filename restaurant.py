from nearby_restaurants import get_nearby_restaurants
from bson.objectid import ObjectId


"""
Restaurant : 
	id
	address
	name
	photo
	Places_id
	party_id

Restaurant_parties:
	restaurant_id
	party_id
	user_id



"""


def initialize_restaurants(db, party):
	print(party)
	location = party['location']
	lat = location['lat']
	lon = location['lng']
	
	res_list = get_nearby_restaurants(lat,lon)
	r_list = []
	for r in res_list:
		r['party_id'] = party['_id']
		r_list.append(r)	
	collection = db['restaurants']
	if not r_list:
		collection.insert_many(r_list)

def update_restaurant_for_user(db, restaurant, user, party):
	res_part = db['restaurant_parties']
	res_part_id = res_part.find_one_and_update(
		{ 'party_id' : party['_id'], 'user_id' : user['id']},
		{ '$set' : { 'restaurant_id' : restaurant['_id']} },
		{ 'upsert' : True} )
	return res_part_id


def get_restaurants_for_party_by_user(db, party_id, username):
	# TODO : Check this after initializing polls
	restaurants = db['restaurants']
	user_restaurants = db['user_restaurants']
	res = collection.find({'party_id' : ObjectId(party_id)})
	for r in res:
		r['_id'] = str(party['_id'])
		result.append(r)
	return result
	
	
