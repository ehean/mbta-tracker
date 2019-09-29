import sys
import curses
import pprint
import requests
import urllib.parse
import datetime
import argparse
import yaml
import constants
from time import sleep
from predictionClass import Predictions

def printToConsole(predictions):
    screen = curses.initscr()
    curses.curs_set(0)
    while True:
        screen.clear()
        screen.addstr(0,0, "Line: " + predictions.route)
        screen.addstr(1,0, "Stop: " + predictions.stop)
        row = 2
        for p in predictions.data:
            displayValue = getDisplayValueFromAttributes(p["attributes"])
            screen.addstr(row, 0, displayValue)
            row = row + 1
        screen.refresh()
        sleep(1)

def validateStreamingResponse(response):
    print(response["event"])
    if response["event"] == "reset": 
        pprint.pprint(response["data"])
        if "data" in response:
            return response["data"][0]
    elif response["event"] == "update":
        if "data" in response:
            return response["data"]
    else:
        return {}

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

def getDisplayValueFromAttributes(attribute):
    displayValue = ""
    status = getStatusFromAttribute(attribute)
    if status == None:
        predictedTime = getPredictedTimeFromAttribute(attribute)
        if predictedTime != None:
#            print(predictedTime)
            secondsAway = getSecondsAwayFromDateTime(predictedTime)
#            print(secondsAway)
            if secondsAway <= 30:
                displayValue = "Arriving"
            elif secondsAway <= 60:
                displayValue = "Approaching"
            elif secondsAway <= 89:
                displayValue = "1 minute"
            else:
                displayValue = str(int(round(secondsAway/60.0))) + " minutes"
    else:
        if status == "STOPPED_AT":
            if secondsAway <= 90:
                displayValue = "Boarding"
            else:
                displayValue = status
        else:
            displayValue = status
    
    return displayValue
            
def getDisplayValueFromPrediction(prediction):
    displayValue = ""
    if prediction["status"] == None or prediction["status"] != "STOPPED_AT":
        if prediction["predictedTime"] != None:
#            print(prediction["predictedTime"])
            secondsAway = getSecondsAwayFromDateTime(prediction["predictedTime"])
#            print(secondsAway)
            if prediction["status"] == "STOPPED_AT":
                if secondsAway <= 90:
                    displayValue = "Boarding"
                else:
                    displayValue = prediction["status"]
            elif secondsAway <= 30:
                displayValue = "Arriving"
            elif secondsAway <= 60:
                displayValue = "Approaching"
            elif secondsAway <= 89:
                displayValue = "1 minute"
            else:
                displayValue = str(int(round(secondsAway/60.0))) + " minutes"
    else:
        displayValue = prediction["status"]
    
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
