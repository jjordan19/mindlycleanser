from flask import Flask, render_template, Response, request
import flask
from markupsafe import escape
import pymongo
import json
from bson import json_util


# Creates MongoDB connection between application and database.
#db = pymongo.MongoClient("mongodb+srv://admin-python-test-app:QSzVf6aJw5XM6t1v@cluster0.vzhrl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
app = Flask(__name__)

# Create mindlycleaser database
try:
    db = pymongo.MongoClient("mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb") # Connects to local MongoDB
except:
    print("ERROR: Connection to MongoDB failed")

database = db["mindlycleanser"]
collection = database["quotes"]

@app.route("/")
def home_page():
    return render_template('index.html', title="MindlyCleanser", all_quotes=list(collection.find({})))

# Create a quote using the REST API
@app.route("/add/<int:quote_id>/<author>/<quote>/")
def add_quote(quote_id, author, quote):
    try:
        quote = quote.replace("-", " ")
        collection.insert_one({"_id": f"{quote_id}", "author": f"{author}", "quote": f"{quote}"})
        return flask.jsonify(message="success")
    except Exception as DuplicateKeyError:
        existing = collection.find({"_id": f"{quote_id}"})
        if existing:
            total = list(collection.find({}))
            len_total = len(total)
            quote_id = len_total + 1
            collection.insert_one({"_id": f"{quote_id}", "author": f"{author}", "quote": f"{quote}"})    
        return flask.jsonify(message=f"New ID: {quote_id}")

# List quotes
@app.route("/quotes")
def list_quote():
    all_quotes = list(collection.find({}))
    return render_template("list_quotes.html", title="MindlyCleanser", quotes=all_quotes)

@app.route("/add/", methods=["GET", "POST"])
def add():
    try:
        if request.method == "POST":
            id_num = request.form.get("quote_id")
            quote = request.form.get("quote_adder")
            author = request.form.get("author_adder")
            query = { "_id" : id_num,"author" : author, "quote" : quote }
            collection.insert(query)
    except:
        pass
    return render_template("add_quotes_form.html", title="MindlyCleanser")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    try:
        if request.method == "POST":
       # getting input with name = fname in HTML form
           id_number = request.form.get("query_id")
       # getting input with name = lname in HTML form
           query = { "_id" : id_number } 
           collection.delete_one(query)
    except:
        pass
    return render_template("delete.html", title="MindlyCleanser")


if __name__ == "__main__":
    app.run(host="10.0.0.14", port=5000, debug=True)
