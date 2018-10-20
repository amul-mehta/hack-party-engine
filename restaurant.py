from nearby_restaurants import get_nearby_restaurants
from bson.objectid import ObjectId
from user import findUserByName


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
	if r_list:
		collection.insert_many(r_list)


def update_restaurant_for_user(db, restaurant_id, user_id, party_id):
	res_part = db['restaurant_parties']
	res_part_id = res_part.find_one_and_update(
		{ 'party_id' : ObjectId(party_id), 'user_id' : ObjectId(user_id)},
		{ '$set' : { 'restaurant_id' : ObjectId(restaurant_id)} },
		{ 'upsert' : True} )
	return res_part_id


def get_restaurants_for_party_by_user(db, party_id, user_id):
	# TODO : Check this after initializing polls
	restaurants = db['restaurants']
	user_restaurants = db['user_restaurants']
	res = collection.find({'party_id' : ObjectId(party_id)})
	choice = user_restaurants.find_one({'user_id': ObjectId(user_id)})['restaurant_id']
	restaurant_list = []
	for r in res:
		r['_id'] = str(r['_id'])
		restaurant_list.append(r)
	result = {
		'restaurants' : restaurant_list,
	 	'user_vote' : str(choice)
	}
	return result
	
	
