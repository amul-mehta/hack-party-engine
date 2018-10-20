from pymongo import MongoClient
import urllib
import pprint


def main():
	client = MongoClient("mongodb+srv://alyakhtar:" + urllib.parse.quote("maximum@123")  + "@cluster0-4ydzi.gcp.mongodb.net/hackparty?retryWrites=true")
	db = client.hackparty
	collection = db['user']
	x = collection.find_one()
	return x


if __name__ == '__main__':
	main()