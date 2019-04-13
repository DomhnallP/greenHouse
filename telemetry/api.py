#!/usr/bin/env python
#Restful api
from flask import Flask
from flask_restful import Resource, Api
import time

app = Flask(__name__)
api = Api(app)

class greenHouseInfo(Resource):
    #This currently returns dummy data
    #TODO make methods return real information
    def get(self):
        return {
            'data': {
                'Temperature':'17',
                'Humidity': '53'
            },
            'metadata': {
                'timestamp' : time.time(),
                'sensorIP' : '0.0.0.0:80'
            }
        }

api.add_resource(greenHouseInfo, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80, debug=True)