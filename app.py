
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index_page():
    return "<p>Welcome, Homie!</p>"

@app.route('/signup')
def signup():
    return 'Sign Up Page'

@app.route('/login')
def hello():
    return 'Login Page'
