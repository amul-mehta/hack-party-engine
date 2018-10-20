import requests

API_KEY = 'AIzaSyAO3elCCuw_r-VxyU-teNy1JzV6ukTjDOQ'
#url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
url ='https://maps.googleapis.com/maps/api/place/textsearch/json'

def get_nearby_restaurants(lat,lon):
	q = 'food near me'
	params = { 'location' : ','.join([lat,lon]), 'radius' : 5000, 'type' : 'food', 'query': q, 'key' : API_KEY}
	contents = requests.get(url, params=params)
	if contents.status_code == 200:
		res = []
		#print(contents.json())
		restaurants = contents.json()['results']
		#print(restaurants)
		for restaurant in restaurants:
			#print(restaurant)
			p_ref = None
			if len(restaurant['photos']) > 0:
				p_ref = restaurant['photos'][0]['photo_reference']	
			res.append({'address' : restaurant['formatted_address'], 'name' : restaurant['name'], 'photo' : p_ref, 'place_id' : restaurant['place_id'] })
		return res	
	return []

#res = get_nearby_restaurants('42.361145','-71.057083')
#print(res)
	
