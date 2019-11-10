from pprint import pprint
import constants
import requests
from log import logger
from circuitbreaker import circuit

class Predictions:
    def __init__(self):
        self.data = {}
        self.idMap = {}
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

        logger.info("Finished creating stop id map.")

    def getParentStopFromChildStop(self, childStopId):
        if childStopId in self.childStopIdMap:
            return self.childStopIdMap[childStopId]
        else:
            return None

    def getPredictionIdFromResponse(self, response):
        return response["id"]

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

    def addPredictionToIdMap(self, resp):
        predictionId = self.getPredictionIdFromResponse(resp)
        if predictionId not in self.idMap:
            self.idMap[predictionId] = {}
            self.idMap[predictionId]["route"]     = self.getRouteIdFromResponse(resp)
            self.idMap[predictionId]["stop"]      = self.getParentStopFromChildStop(self.getChildStopIdFromResponse(resp))
            self.idMap[predictionId]["direction"] = self.getDirectionIdFromResponse(resp)

    def addPredictionToData(self, resp):
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
 
    def eventHandler(self, response):
        if response["event"] == "reset":
            logger.debug("RESET event received.")
            self.handleResetEvent(response)
        elif response["event"] == "update":
            logger.debug("UPDATE event received.")
            self.handleUpdateEvent(response["data"])
        elif response["event"] == "add":
            logger.debug("ADD event received.")
            self.handleAddEvent(response["data"])
        elif response["event"] == "remove":
            logger.debug("REMOVE event received.")
            self.handleRemoveEvent(response["data"])

    def handleResetEvent(self, response):
        self.createStopIdMaps()
        for resp in response["data"]:
            self.addPredictionToIdMap(resp)
            self.addPredictionToData(resp)
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
        for pred in self.data[route][parentStop][direction]:
            logger.debug(pred)
            if pred["id"] == resp["id"]:
                logger.debug("Found prediction to update.")
                pred.update(resp)

    def handleAddEvent(self, resp):
        self.addPredictionToIdMap(resp)
        self.addPredictionToData(resp)
       
    def handleRemoveEvent(self, resp):
        pId = resp["id"]
        if pId in self.idMap:
            route = self.idMap[pId]["route"]
            if route in self.data:
                stop = self.idMap[pId]["stop"]
                if stop in self.data[route]:
                    direction = self.idMap[pId]["direction"]
                    if direction in self.data[route][stop]:
                        directionList = self.data[route][stop][direction]
                        for index, prediction in enumerate(directionList):
                            if prediction["id"] == resp["id"]:
                                directionList.pop(index)
                                self.idMap.pop(pId, None)

predictions = Predictions()

