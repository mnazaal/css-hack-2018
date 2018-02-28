from flask import Flask, render_template, request
#from flask_googlemaps import GoogleMaps
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

api = Api(app)

#app.config['GOOGLEMAPS_KEY'] = "8JZ7i18MjFuM35dJHq70n3Hx4"

#GoogleMaps(app)

#GoogleMaps(app, key="8JZ7i18MjFuM35dJHq70n3Hx4")

@app.route('/')
def index():
    return render_template("index.html")

longitude = 51.508742
latitude = -0.120850
@app.route('/', methods = ['POST'])
def PostHandler():
    data = request.get_data()
    return str(data)
#class Signal(Resource):
    
