from flask import Flask, render_template
#from flask_googlemaps import GoogleMaps

app = Flask(__name__)

#app.config['GOOGLEMAPS_KEY'] = "8JZ7i18MjFuM35dJHq70n3Hx4"

#GoogleMaps(app)

#GoogleMaps(app, key="8JZ7i18MjFuM35dJHq70n3Hx4")

@app.route('/')
def index():
    return render_template("index.html")



