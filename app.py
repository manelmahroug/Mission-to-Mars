from flask import Flask, render_template, jsonify, redirect
import PyMongo
import pymongo
import scrape_mars

 

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn) 
mars_db=client.marsScrape_DB
collection = db.mars_info


@app.route("/")
def index():
    marsScrape_Data = db.mars_info.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    marsDb = mars_db.mars_info
    marsDb.update(
        {},
        mars_data,
        upsert=True
    )


    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

 
