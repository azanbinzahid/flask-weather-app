from flask import Flask, render_template, request
import pyrebase
from config import firebaseAPI

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


# init db
# data = {
#     "cities" : [
#         {"name": "Lahore"},
#         {"name": "London"},
#         {"name": "Dehli"},
#     ]
# }
# db.set(data)


@app.route("/", methods =["GET", "POST"])
def index():
    if request.method=="POST":
        name = request.form["name"]
        if name:
            data = {
                "name": name
            }
            db.child("cities").push(data)

    cities = db.child("cities").get().val()
    return render_template("index.html", cities = cities)



if __name__ == '__main__':
    app.run()