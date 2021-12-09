from flask import Flask, render_template, Response
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
    return render_template('index.html', title="MindlyCleanser")

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
def get_quote():
    all_quotes = list(collection.find({}))
    return json.dumps(all_quotes)

@app.route("/delete")
def delete_quote():
    return "delete something!"









if __name__ == "__main__":
    app.run(host="10.0.0.14", port=5000, debug=True)
