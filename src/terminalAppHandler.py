import sys
import curses
from pprint import pprint
import datetime
import yaml
import constants
from time import sleep

def printToConsole(predictions):
    screen = curses.initscr()
    curses.curs_set(0)
    while True:
        screen.clear()
        screen.addstr(0,0, "Line: " + predictions.route)
        screen.addstr(1,0, "Stop: " + predictions.stop)
        row = 2
        for p in predictions.data:
            displayValue = getDisplayValueFromAttribute(p["attributes"])
            screen.addstr(row, 0, displayValue)
            row = row + 1
        screen.refresh()
        sleep(1)

def printResponseDetails(response):
    print(response.status_code)
    print(response.headers)
    print(response.request.url)
    pprint.pprint(response.json())

def getPredictedTimeFromAttribute(attribute):
    predictedTime = None
    if "arrival_time" in attribute and attribute["arrival_time"] != None:
        predictedTime = attribute["arrival_time"]
    elif "departure_time" in attribute and attribute["departure_time"] != None:
        predictedTime = attribute["departure_time"]

    if predictedTime != None:
        predictedTime = datetime.datetime.fromisoformat(predictedTime)

    return predictedTime

def getPredictedIsoTimeFromAttribute(attribute):
    predictedTime = None
    if "arrival_time" in attribute and attribute["arrival_time"] != None:
        predictedTime = attribute["arrival_time"]
    elif "departure_time" in attribute and attribute["departure_time"] != None:
        predictedTime = attribute["departure_time"]

    return predictedTime


def getDisplayValueFromAttribute(attribute):
    displayValue = ""
    if attribute != None:
        status = getStatusFromAttribute(attribute)
        if status == None: 
            predictedTime = getPredictedTimeFromAttribute(attribute)
            if predictedTime != None:
                secondsAway = getSecondsAwayFromDateTime(predictedTime)
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
                predictedTime = getPredictedTimeFromAttribute(attribute)
                if predictedTime != None:
                    secondsAway = getSecondsAwayFromDateTime(predictedTime)
                    if secondsAway <= 90:
                        displayValue = "Boarding"
                    else:
                        displayValue = status
                else:
                    displayValue = status
            else:
                displayValue = status
    
    return displayValue
            
def getStatusFromAttribute(attribute):
    if "status" in attribute:
        return attribute["status"]  
    else:
        return None
    
def getSecondsAwayFromDateTime(time):
    if time != None:
        now = datetime.datetime.now()
        now = now.replace(tzinfo=constants.UTC_ZONE)
        now = now.astimezone(constants.EST_ZONE)
        return (time - now).total_seconds()
    else:
        return None
