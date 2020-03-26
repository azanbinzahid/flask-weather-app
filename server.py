from flask import Flask, render_template, request, redirect, url_for
import pyrebase
import requests
from config import firebaseAPI, openweathermapAPI

app = Flask(__name__)
app.config["DEBUG"] = True

config = {
    "apiKey" : firebaseAPI,
    "authDomain": "flask-weather-app-5f470.firebaseapp.com",
    "storageBucket":"flask-weather-app-5f470.appspot.com",
    "databaseURL" : "https://flask-weather-app-5f470.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

cityweather= "http://api.openweathermap.org/data/2.5/weather?q={}&app_id=" + openweathermapAPI

# init db
# data = {
#     "cities" : [
#         {"name": "Lahore"},
#         {"name": "London"},
#         {"name": "Dehli"},
#     ]
# }
# db.set(data)


@app.route("/")
def index():
    cities = db.child("cities").get().val()
    return render_template("index.html", cities = cities)

@app.route("/addcity", methods =["GET", "POST"])
def addCity():
    if request.method=="POST":
        name = request.form["name"]
        if name:
            data = {
                "name": name
            }
            db.child("cities").push(data)
    return redirect(url_for('index'))

@app.route("/weather")
def getWeather():
    cities = db.child("cities").get().val()

    allData = []
    for city in cities.values():
        data = requests.get(cityweather.format(city['name'])).json()
        allData.append(data)
    
    print (allData)
    return "done"

@app.route("/deletecity", methods=['POST'])
def deleteCity():
    city_id = request.form['city_id']
    db.child("cities").child(city_id).remove()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()