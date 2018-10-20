from pymongo import MongoClient
import urllib

def initializeDatabase():
	client = MongoClient("mongodb+srv://alyakhtar:" + urllib.parse.quote("maximum@123")  + "@cluster0-4ydzi.gcp.mongodb.net/hackparty?retryWrites=true")
	db = client.hackparty
	return db