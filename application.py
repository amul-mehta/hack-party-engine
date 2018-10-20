from flask import Flask
from database import main

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/connect")
def connect():
	return main()
