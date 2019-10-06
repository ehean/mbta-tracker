import constants
from predictionClass import predictions
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json

def initClientApi():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Prediction, '/prediction')
    app.run(port='5002')

class Response:
    def __init__(self):
        self.body = { "data": [] }

    def setBody(self, args):
        for p in predictions.data:
            if args["route"] == p["relationships"]["route"]["data"]["id"]:
                if args["stop"] == p["relationships"]["stop"]["data"]["id"]:
                    if args["direction"] == p["attributes"]["direction_id"]:
                        respData = {
                            "status": p["attributes"]["status"],
                            "predictedTime": getPredictedIsoTimeFromAttribute(p["attributes"]),
                            "alert": None
                        }
                        self.body["data"].append(respData)

class Prediction(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('stop')
        self.parser.add_argument('route')
        self.parser.add_argument('direction')
    def get(self):
        args = self.parser.parse_args() 
        resp = Response()
        resp.setBody(args)
        return json.dumps(resp.body)

def getPredictedIsoTimeFromAttribute(attribute):
    predictedTime = None
    if "arrival_time" in attribute and attribute["arrival_time"] != None:
        predictedTime = attribute["arrival_time"]
    elif "departure_time" in attribute and attribute["departure_time"] != None:
        predictedTime = attribute["departure_time"]

    return predictedTime
