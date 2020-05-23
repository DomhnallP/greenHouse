

#Restful api
from flask import Flask, render_template, Markup
from flask_restful import Resource, Api, reqparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import os
import sys
import json

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


class greenHouseInfo(Resource):

    def get(self):
        client = gspread.authorize(creds)
        sheet = client.open("greenHouse_telemetry").sheet1
        jsonObj = {
                "metadata": {
                    'timeRetrieved': time.time()*1000
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
        insertRow= [time.time()*1000, args['temp'], args['humidity']]
        client = gspread.authorize(creds)
        sheet = client.open("greenHouse_telemetry").sheet1
        sheet.insert_row(insertRow, 1)
        return insertRow, 201

@app.route('/dashboard')
def dashboard():
    client = gspread.authorize(creds)
    sheet = client.open("greenHouse_telemetry").sheet1
    data = [
         [int(x),float(y)] for x,y in zip(sheet.col_values(1), sheet.col_values(2))
      ]
    print(data)
    return render_template('index.html', token=data)
        
api.add_resource(greenHouseInfo, '/telemetryCRUD')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80, debug=True)