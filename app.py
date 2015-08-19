from flask import Flask
from flask import render_template
from flask import Response
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps
import json
import pycountry 
import ConfigParser 

app = Flask(__name__,static_folder='static', static_url_path="/static")

config = 'gmaps.key'

@app.route("/")
def index():
	the_list = [ i for i in range(100) ]
        parser = ConfigParser.SafeConfigParser()
        parser.read(config)
        KEY=parser.get('KEYS', 'KEY')
        return render_template("index.html", KEY=KEY, the_list=the_list)

@app.route("/kml")
def return_kml():
	xml = open('static/kml/doc.kml')
	return Response(xml, mimetype='text/xml')

@app.route("/test")	
def test():
	return render_template("test.html")

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5001, debug=True) 


