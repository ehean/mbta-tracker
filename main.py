import sys
import signal
import requests
import urllib.parse
import argparse
import constants
import streamData
import sendToClient
import threading
from predictionClass import Predictions
import curses


def argumentParser():
    argParser = argparse.ArgumentParser("This Python script returns the next predicted departure time for an MBTA for a given stop and routle")
    argParser.add_argument("-s", "--stop", help="This is the stop to provide (e.g. North+Station)", action="store")
    argParser.add_argument("-r", "--route", help="This is the route to provide (e.g. CR-Lowell)", action="store")
    argParser.add_argument("-d", "--direction", help="This is the direction [outbound|inbound]", action="store")
    args = argParser.parse_args()
    return args

def sendRequest(path, requestParams):
    response = requests.get(
        constants.MBTA_API_ENDPOINT + path,
        headers=constants.REQUEST_HEADER_REQ,
        timeout=(constants.CONNECTION_TIMEOUT, constants.RESPONSE_TIMEOUT),
        params=requestParams,
        stream=False
    )
    return response

def validateArguments(args):
    if args.direction not in constants.DIRECTION_MAP:
        raise Exception("Provided direction " + args.direction + " is not a valid direction.")
    if args.route not in constants.ROUTE_LIST:
        raise Exception("Provided route " + args.route + " is not a valid route.")

def getStopId(args):
    stopRequestParams={"filter[route]": args.route}
    stopResponse = sendRequest("stops", stopRequestParams)
    if stopResponse.status_code == 200:
        stopResponse = stopResponse.json()
        for stop in stopResponse["data"]:
            if stop["attributes"]["name"] == args.stop:
                return stop["id"] 
        raise Exception("Could not find stop " + args.stop + " in route " + args.route + ".")
    else:
        print(response.request.url)
        raise Exception("/stops request failed.") 

def getRequestParams(args):
    validateArguments(args)

    stopId=urllib.parse.unquote_plus(getStopId(args))
    route=urllib.parse.unquote_plus(args.route)
    direction=constants.DIRECTION_MAP[args.direction]
    requestParams={
        "filter[stop]": stopId,
        "filter[route]": route,
        "filter[direction_id]": direction
    }
    return requestParams

def signalHandler(sig, frame):
    curses.endwin()
    sys.exit(0)

signal.signal(signal.SIGINT, signalHandler)

args = argumentParser()
requestParams = getRequestParams(args)

predictions = Predictions(args.route, args.stop)
streamingThread = threading.Thread(target=streamData.openStreaming, args=("predictions", requestParams, predictions))
clientThread = threading.Thread(target=sendToClient.printToConsole, args=(predictions,))

streamingThread.start()
clientThread.start()

streamingThread.join()
streamingThread.join()
