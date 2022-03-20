# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)



# create route that renders index.html template
@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    #mars_info = mongo.db.mars_collection.find_one()
    return render_template("index.html", text = "Mission to Mars", mars_data=mars)

# create scrape route 
@app.route("/scrape")
def scrape():
    # run the scrape function
    mars_data = scrape_mars.scrape()

    # insert the mars data into the mongo database
    mongo.db.mars.update_one({}, {"$set": mars_data}, upsert=True)

    # go back to the home page
    return redirect("/", code=302)

    

if __name__ == "__main__":
    app.run(debug=True)
