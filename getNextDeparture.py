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

def getPredictedTimeFromAttribute(attribute):
    if "departure_time" in attribute and attribute["departure_time"] != None:
        if "arrival_time" in attribute and attribute["arrival_time"] != None:
            predictedTime = attribute["arrival_time"]
        else:
            predictedTime = attribute["departure_time"]
        
        predictedTime = datetime.datetime.fromisoformat(predictedTime)
        return predictedTime

def getDisplayValueFromAttribute(attribute):
    displayValue = ""
    status = getStatusFromAttribute(attribute)
    if status == None or status != "STOPPED_AT":
        predictedTime = getPredictedTimeFromAttribute(attribute)
        if predictedTime != None:
            print(predictedTime)
            secondsAway = getSecondsAwayFromDateTime(predictedTime)
            print(secondsAway)
            if status == "STOPPED_AT":
                if secondsAway <= 90:
                    displayValue = "Boarding"
                else:
                    displayValue = status
            elif secondsAway <= 30:
                displayValue = "Arriving"
            elif secondsAway <= 60:
                displayValue = "Approaching"
            elif secondsAway <= 89:
                displayValue = "1 minute"
            else:
                displayValue = str(int(round(secondsAway/60.0))) + " minutes"
    else:
        displayValue = status
    
    return displayValue
            
             
     
                
def printNextDepartureTimeFromDatetime(time):
    if time != None:
        print(time.strftime("%I:%M %p"))

def getStatusFromAttribute(attribute):
    return attribute["status"]  
    
def printStatus(status):
    if status != None:
        print(status)

def getSecondsAwayFromDateTime(time):
    if time != None:
        now = datetime.datetime.now()
        now = now.replace(tzinfo=constants.UTC_ZONE)
        now = now.astimezone(constants.EST_ZONE)
        return (time - now).total_seconds()
    else:
        return None
        

args = argumentParser()
requestParams = getRequestParams(args)
response = sendRequest("predictions", requestParams)
#printResponseDetails(response)
data = validateResponse(response)
if data != []:
    displayValue = getDisplayValueFromAttribute(data[0]["attributes"])
    print(displayValue)
