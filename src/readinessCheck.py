from predictionClass import predictions
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pprint import pprint

def initReadinessCheck():
    print("Initializing Readiness check")
    app = Flask(__name__)
    readinessCheck = Api(app)
    readinessCheck.add_resource(Readiness, '/readiness')
    app.run(port='6000', host='0.0.0.0')

class Readiness(Resource):
    def get(self):
        if predictions.ready == True:
            return { "Ready": "True" }, 200
        else:
            return { "Ready": "False" }, 400
