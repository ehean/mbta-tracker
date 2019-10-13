from pprint import pprint
import constants
import requests
from circuitbreaker import circuit

class Predictions:
    def __init__(self):
        self.data = {}
        self.stopIdMap = {}
        self.childStopIdMap = {}
        self.ready = False
    
    @circuit(failure_threshold=5, expected_exception=requests.RequestException)
    def sendRequest(self, path, requestParams):
        response = requests.get(
            constants.MBTA_API_ENDPOINT + path,
            headers=constants.REQUEST_HEADER_REQ,
            timeout=(constants.CONNECTION_TIMEOUT, constants.RESPONSE_TIMEOUT),
            params=requestParams,
            stream=False
        )
        return response
    
    def createStopIdMaps(self):
        stopRequestParams={
            "filter[route]": constants.ROUTES,
            "include": "child_stops"
        }
        stopResponse = self.sendRequest("stops", stopRequestParams)
        if stopResponse.status_code == 200:
            stopResponse = stopResponse.json()
            for stop in stopResponse["data"]:
                self.stopIdMap[stop["id"]] = {
                    "name": stop["attributes"]["name"],
                    "child_stops": stop["relationships"]["child_stops"]["data"]
                }
                for child_stop in stop["relationships"]["child_stops"]["data"]:
                    self.childStopIdMap[child_stop["id"]] = stop["id"]    
        else:
            print(response.request.url)
            raise Exception("/stops request failed.")

    def getParentStopFromChildStop(self, childStopId):
        if childStopId in self.childStopIdMap:
            return self.childStopIdMap[childStopId]
        else:
            return None

    def getRouteIdFromResponse(self, response):
        return response["relationships"]["route"]["data"]["id"]

    def getChildStopIdFromResponse(self, response):
        return response["relationships"]["stop"]["data"]["id"]

    def getDirectionIdFromResponse(self, response):
        return response["attributes"]["direction_id"]

    def getStopIdFromChildStopId(self, childStopId):
        for stop in self.included:
            if stop["id"] == stopId:
                return stop["attributes"]["name"]

    def eventHandler(self, response):
        if response["event"] == "reset":
            self.handleResetEvent(response)
        elif response["event"] == "update":
            self.handleUpdateEvent(response["data"])
        elif response["event"] == "add":
            self.handleAddEvent(response["data"])
        elif response["event"] == "remove":
            self.handleRemoveEvent(response["data"])

    def handleResetEvent(self, response):
        self.createStopIdMaps()
        for resp in response["data"]:
            route = self.getRouteIdFromResponse(resp)
            if route not in self.data:
                self.data[route] = {}
            parentStop = self.getParentStopFromChildStop(self.getChildStopIdFromResponse(resp))
            if parentStop != None:
                if parentStop not in self.data[route]:
                    self.data[route][parentStop] = {}
                direction = self.getDirectionIdFromResponse(resp)
                if direction not in self.data[route][parentStop]:
                    self.data[route][parentStop][direction] = []
                self.data[route][parentStop][direction].append(resp)
        self.ready = True
                
    def handleUpdateEvent(self, resp):
        route = self.getRouteIdFromResponse(resp)
        if route not in self.data:
            self.data[route] = {}
        parentStop = self.getParentStopFromChildStop(self.getChildStopIdFromResponse(resp))
        if parentStop not in self.data[route]:
            self.data[route][parentStop] = {}
        direction = self.getDirectionIdFromResponse(resp)
        if direction not in self.data[route][parentStop]:
            self.data[route][parentStop][direction] = []
        self.data[route][parentStop][direction].append(resp)
        for pred in self.data[route][parentStop][direction]:
            if pred["id"] == resp["id"]:
                pred = resp

    def handleAddEvent(self, resp):
        route = self.getRouteIdFromResponse(resp)
        if route not in self.data:
            self.data[route] = {}
        parentStop = self.getParentStopFromChildStop(self.getChildStopIdFromResponse(resp))
        if parentStop not in self.data[route]:
            self.data[route][parentStop] = {}
        direction = self.getDirectionIdFromResponse(resp)
        if direction not in self.data[route][parentStop]:
            self.data[route][parentStop][direction] = []
        self.data[route][parentStop][direction].append(resp)
       
    def handleRemoveEvent(self, resp):
        for route in self.data.values():
            for stop in route.values():
                for direction in stop.values():
                    for index, prediction in enumerate(direction):
                        if prediction["id"] == resp["id"]:
                            direction.pop(index)

predictions = Predictions()

