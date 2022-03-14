# import necessary libraries
from flask import Flask, render_template

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/")
def home():
    mars_info =
    return render_template("index.html", list=mars_info)

# create scrape route 
@app.route("/scrape")
def scrape():
    # run the scrape function
    #mars_data = scrape_mars.scrape()

    # insert the mars data in to the collection
    #mongo.db.mars_collection.update({}, mars_data, upsert=True)

    # go back to the home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
