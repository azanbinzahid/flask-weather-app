from flask import Flask, render_template, request
from os import path
app = Flask(__name__)

app.config["DEBUG"] = True

cities = set()


@app.route("/", methods =["GET", "POST"])
def index():
    if request.method=="POST":
        name = request.form["name"]
        cities.add(name)
        return render_template('index.html', names = cities)
    return render_template("index.html", names = cities)



if __name__ == '__main__':
    app.run()