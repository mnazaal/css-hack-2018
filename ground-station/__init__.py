from flask import Flask, render_template, request
#from flask_googlemaps import GoogleMaps
from flask_restful import Resource, Api, reqparse
import reverse_geocoder as rg

app = Flask(__name__)

api = Api(app)

#app.config['GOOGLEMAPS_KEY'] = "8JZ7i18MjFuM35dJHq70n3Hx4"

#GoogleMaps(app)

#GoogleMaps(app, key="8JZ7i18MjFuM35dJHq70n3Hx4")

@app.route('/')
def index():
    #data = request.get_data()
    #data = data.decode()
    #data = data.split("&")
    #latitude, longitude = data[5].split("=")[1], data[6].split("=")[1]
    latitude, longitude = 51.508742, -0.120850
    loc = {"lat": latitude, "lng": longitude}
    return render_template("index.html", loc=loc)
   
@app.route('/', methods = ['POST'])
def PostHandler():
    data = request.get_data()
    print(str(data))
    data = data.decode()
    data = data.split("&")
    latitude, longitude = data[5].split("=")[1], data[6].split("=")[1]
    print(latitude)
    print(longitude)
    loc = {"lat": latitude, "lng": longitude}
    locextra = rg.search((latitude, longitude))[0]
    area = locextra['name']
    country = locextra['admin1']
    print(str(area + ', ' + country))
    return render_template("index.html", loc=loc)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4040,  debug=True)
