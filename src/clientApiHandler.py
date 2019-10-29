import constants
from predictionClass import predictions
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from pprint import pprint
import requests

def initClientApi():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Prediction, '/prediction')
    app.run(port='443', host='0.0.0.0')

class Response:
    def __init__(self):
        self.body = { "data": [] }

    def setBody(self, args):
        if args["route"] in predictions.data:
            if args["stop"] in predictions.data[args["route"]]:
                if int(args["direction"]) in predictions.data[args["route"]][args["stop"]]:
                    for p in predictions.data[args["route"]][args["stop"]][int(args["direction"])]:
                        respData = {
                            "status": p["attributes"]["status"],
                            "predictedTime": getPredictedIsoTimeFromAttribute(p["attributes"]),
                            "alert": None
                        }
                        self.body["data"].append(respData)
                else:
                    self.body = { "error": "Direction Id " + str(args["direction"]) + " not found."}
            else:
                self.body = { "error": "Stop Id " + args["stop"] + " not found."}
        else:
            self.body = { "error": "Route Id " + args["route"] + " not found."}

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
        return jsonify(resp.body)

def getPredictedIsoTimeFromAttribute(attribute):
    predictedTime = None
    if "arrival_time" in attribute and attribute["arrival_time"] != None:
        predictedTime = attribute["arrival_time"]
    elif "departure_time" in attribute and attribute["departure_time"] != None:
        predictedTime = attribute["departure_time"]

    return predictedTime

