from flask import Flask, render_template
from markupsafe import escape
import pymongo

# Creates MongoDB connection between application and database.
db = pymongo.MongoClient("mongodb+srv://admin-python-test-app:QSzVf6aJw5XM6t1v@cluster0.vzhrl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

app = Flask(__name__)

@app.route("/login")
def login():
    return "login"

@app.route("/")
def mindlycleanser():
    return render_template('index.html', welcome='Welcome, to my newly created app!')

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'
