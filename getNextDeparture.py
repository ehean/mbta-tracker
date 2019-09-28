import pprint
import requests
import urllib.parse
import datetime
import argparse
import constants
import routesMap



def argumentParser():
    argParser = argparse.ArgumentParser("This Python script returns the next predicted departure time for an MBTA for a given stop and routle")
    argParser.add_argument("-s", "--stop", help="This is the stop to provide (e.g. North+Station)", action="store")
    argParser.add_argument("-r", "--route", help="This is the route to provide (e.g. CR-Lowell)", action="store")
    argParser.add_argument("-d", "--direction", help="This is the direction [outbound|inbound]", action="store")
    args = argParser.parse_args()
    return args

def validateArguments(args):
    if args.direction not in constants.DIRECTION_MAP:
        raise Exception("Provided direction " + args.direction + " is not a valid direction.")
    if args.route not in routesMap.ROUTES_MAP:
        raise Exception("Provided route " + args.route + " is not a valid route.")
    if args.stop not in routesMap.ROUTES_MAP[args.route]:
        raise Exception("Provided stop " + args.stop + " is not in route: " + args.route + ".")

def getRequestParams(args):
    validateArguments(args)

    stop=urllib.parse.unquote_plus(routesMap.ROUTES_MAP[args.route][args.stop])
    route=urllib.parse.unquote_plus(args.route)
    direction=constants.DIRECTION_MAP[args.direction]
    requestParams={
        "filter[stop]": stop,
        "filter[route]": route,
        "filter[direction_id]": direction
    }
    return requestParams

def sendRequest(args):
    requestParams = getRequestParams(args)
    response = requests.get(
        constants.MBTA_API_ENDPOINT + "predictions/",
        headers=constants.REQUEST_HEADER,
        params=requestParams
    )
    return response

def validateResponse(response):
    if response.status_code == 200:
        responseJson = response.json()
        if "data" in responseJson:
            data = responseJson["data"]
            if data != []:
                attributes = data[0]["attributes"]
                return attributes

def printResponseDetails(response):
    print(response.status_code)
    print(response.headers)
    print(response.request.url)
    pprint.pprint(response.json())

def printNextDepartureTime(response):
    attributes = validateResponse(response)

    if attributes != None:
        if "departure_time" in attributes and attributes["departure_time"] != None:
            if "arrival_time" in attributes and attributes["arrival_time"] != None:
                departureTime = attributes["arrival_time"]
            else:
                departureTime = attributes["departure_time"]
            
            departureTime = datetime.datetime.fromisoformat(departureTime)
            departureTime = departureTime.time()
            print("Departure Time: ")
            print(departureTime.strftime("%I:%M %p"))


args = argumentParser()
response = sendRequest(args)
printResponseDetails(response)
printNextDepartureTime(response)
