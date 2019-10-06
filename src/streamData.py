import sys
import curses
import pprint
import requests
import urllib.parse
import datetime
import argparse
import yaml
import constants
from predictionClass import Predictions
from predictionClass import predictions


def openStreaming(resource, requestParams):
    response = sendStreamingRequest(resource, requestParams)
    
    event=""
    totalBytes=0
    
    print("Starting ...")
    for line in response.iter_lines():
        # filter out keep-alive new lines
        if line:
            decodedLine = line.decode('utf-8')
            totalBytes = totalBytes + len(decodedLine)
            if decodedLine.startswith('event:'):
                event = yaml.load(decodedLine, Loader=yaml.FullLoader)
            elif decodedLine.startswith(': keep-alive'):
                keepAlive=True
            else:
                data = {'event':event['event'], 'data':yaml.load(decodedLine, Loader=yaml.FullLoader)['data']}
                predictions.eventHandler(data)

def sendStreamingRequest(path, requestParams):
    response = requests.get(
        constants.MBTA_API_ENDPOINT + path,
        headers=constants.REQUEST_HEADER_STREAM,
        timeout=(constants.CONNECTION_TIMEOUT, constants.RESPONSE_TIMEOUT),
        params=requestParams,
        stream=True
    )
    return response
