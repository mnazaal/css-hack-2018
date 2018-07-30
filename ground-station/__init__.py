from flask import Flask, render_template, request, jsonify
#from flask_googlemaps import GoogleMaps
from flask_restful import Resource, Api, reqparse
import reverse_geocoder as rg

app = Flask(__name__)

api = Api(app)


#GoogleMaps(app)


loc = ""

@app.route('/')
def index():
    #data = request.get_data()
    #data = data.decode()
    #data = data.split("&")
    #latitude, longitude = data[5].split("=")[1], data[6].split("=")[1]
    latitude, longitude = 51.455593, -2.603691
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
    global loc
    loc = {"lat": latitude, "lng": longitude}
    locextra = rg.search((latitude, longitude))[0]
    area = locextra['name']
    country = locextra['admin1']
    print(str(area + ', ' + country))
    print("===")
    print(loc)
    return jsonify(loc=loc)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4040,  debug=True)
