

#Restful api
from flask import Flask
from flask_restful import Resource, Api, reqparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import os
import sys

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('temp')
parser.add_argument('humidity')

#Google spreadsheets api - using a google sheet as a backend for prototyping
scope = ["https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]
basedir = os.path.abspath(os.path.dirname(__file__))
data_json = basedir+'/key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(data_json, scope)
client = gspread.authorize(creds)
sheet = client.open("greenHouse_telemetry").sheet1

class greenHouseInfo(Resource):

    def get(self):
        jsonObj = {
                "metadata": {
                    'timeRetrieved': time.time(),
                },
                'data':{
                    'timeStamps':sheet.col_values(1),
                    'tempData': sheet.col_values(2),
                    'humidityData': sheet.col_values(3) 
                }
        }
        return jsonObj
    
    def post(self):
        args = parser.parse_args()
        insertRow= [time.time(), args['temp'], args['humidity']]
        sheet.insert_row(insertRow, 1)
        return insertRow, 201
        
api.add_resource(greenHouseInfo, '/telemetry')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80, debug=True)