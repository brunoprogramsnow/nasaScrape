from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/nasa_app")

@app.route("/")
def home():

    # Find one record of data from the mongo database
    db_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_data = db_data)


@app.route("/scrape")
def scrape():

    # Run the scrape function
    data = scrape.runScrape()

    #drops collection for duplicates
    mongo.db.mars_data.drop()

    # Insert the Mongo database 
    mongo.db.mars_data.insert(data)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)