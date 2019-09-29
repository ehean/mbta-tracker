import pprint
import requests
import urllib.parse
import datetime
import argparse
import constants



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
        headers=constants.REQUEST_HEADER,
        params=requestParams
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


def validateResponse(response):
    if response.status_code == 200:
        responseJson = response.json()
        if "data" in responseJson:
            return responseJson["data"]

def printResponseDetails(response):
    print(response.status_code)
    print(response.headers)
    print(response.request.url)
    pprint.pprint(response.json())

def getNextDepartureTime(attribute):
    if "departure_time" in attribute and attribute["departure_time"] != None:
        if "arrival_time" in attribute and attribute["arrival_time"] != None:
            departureTime = attribute["arrival_time"]
        else:
            departureTime = attribute["departure_time"]
        
        departureTime = datetime.datetime.fromisoformat(departureTime)
        return departureTime.time()
                
def printNextDepartureTime(time):
    if time != None:
        print(time.strftime("%I:%M %p"))

def getStatus(attribute):
    return attribute["status"]  
    
def printStatus(status):
    if status != None:
        print(status)


args = argumentParser()
requestParams = getRequestParams(args)
response = sendRequest("predictions", requestParams)
#printResponseDetails(response)
data = validateResponse(response)
if data != []:
    time = getNextDepartureTime(data[0]["attributes"])
    printStatus(getStatus(data[0]["attributes"]))
    printNextDepartureTime(time)
