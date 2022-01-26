from flask import Flask, render_template, Response, request, url_for, redirect, session
import flask, pymongo, bcrypt, os, json
from markupsafe import escape
from bson import json_util

# initialize flask app
app = Flask(__name__)

# The secret key is needed to keep the client-side sessions secure
secret = os.urandom(12).hex()
app.secret_key = secret

# Create mindlycleaser database connection between app and db
try:
    db = pymongo.MongoClient("mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb") # Connects to local MongoDB
except:
    print("ERROR: Connection to MongoDB failed")


# Create mindlycleanser db, quote and user collection 
database = db["mindlycleanser"]
quote_collection = database["quotes"]
user_collection = database["users"]

# Create register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    message = ''
    if "username" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        user = request.form.get("fullname")
        username = request.form.get("username")
        
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user_found = user_collection.find_one({"name": user})
        username_found = user_collection.find_one({"username": username})

        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)

        if username_found:
            message = 'This username already exists in database'
            return render_template('register.html', message=message)

        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'username': username, 'password': hashed}
            user_collection.insert_one(user_input)
            
            user_data = user_collection.find_one({"username": username})
            new_username = user_data['username']
   
            return render_template('logged_in.html', username=new_username)
    return render_template('register.html')

# Creates Index Page (Home page)
@app.route('/')
@app.route('/logged_in')
def index():
    if "username" in session:
        username = session["username"]
        return render_template('index.html', title="MindlyCleanser", all_quotes=list(quote_collection.find({})))
    else:
        return redirect(url_for("login"))

# Creates a login page
@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "username" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

       
        username_found = user_collection.find_one({"username": username})

        if username_found:
            username_val = username_found['username']
            passwordcheck = username_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["username"] = username_val
                return redirect(url_for('index'))
            else:

                if "username" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Username not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

# Create a logout page
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "username" in session:
        session.pop("username", None)
        return render_template("signout.html")
    else:
        return render_template('login.html')

# Create a quote using the REST API
@app.route("/add/<int:quote_id>/<author>/<quote>/")
def add_quote(quote_id, author, quote):
    try:
        quote = quote.replace("-", " ")
        quote_collection.insert_one({"_id": f"{quote_id}", "author": f"{author}", "quote": f"{quote}"})
        return flask.jsonify(message="success")
    except Exception as DuplicateKeyError:
        existing = quote_collection.find({"_id": f"{quote_id}"})

        if existing:
            total = list(quote_collection.find({}))
            len_total = len(total)
            quote_id = len_total + 1
            quote_collection.insert_one({"_id": f"{quote_id}", "author": f"{author}", "quote": f"{quote}"})    
        return flask.jsonify(message=f"New ID: {quote_id}")

# List quotes
@app.route("/quotes/")
def list_quote():
    all_quotes = list(quote_collection.find({}))
    return render_template("list_quotes.html", title="MindlyCleanser", quotes=all_quotes)

@app.route("/add/", methods=["GET", "POST"])
def add():
    try:
        if request.method == "POST":
            id_num = request.form.get("quote_id")
            quote = request.form.get("quote_adder")
            author = request.form.get("author_adder")
            query = { "_id" : id_num,"author" : author, "quote" : quote }
            quote_collection.insert(query)
    except:
        pass
    return render_template("add_quotes_form.html", title="MindlyCleanser")

@app.route("/delete/", methods=["GET", "POST"])
def delete():
    try:
        if request.method == "POST":
       # getting input with name = fname in HTML form
           id_number = request.form.get("query_id")
       # getting input with name = lname in HTML form
           query = { "_id" : id_number } 
           quote_collection.delete_one(query)
    except:
        pass
    return render_template("delete.html", title="MindlyCleanser")

if __name__ == "__main__":
    app.run(host="10.0.0.14", port=5000, debug=True)
