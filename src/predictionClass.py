
class Predictions:
    def __init__(self):
        self.data = []
        self.route = ""
        self.stop = ""

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
        self.data = response["data"]

    def handleUpdateEvent(self, response):
        for prediction in self.data:
            if prediction["id"] == response["id"]:
                prediction["attributes"] = response["attributes"]
                prediction["relationships"] = response["relationships"]

    def handleAddEvent(self, response):
        self.data.append(response)
    
    def handleRemoveEvent(self, response):
        for prediction in self.data:
            if prediction["id"] == response["id"]:
                self.data.remove(prediction)

predictions = Predictions()

