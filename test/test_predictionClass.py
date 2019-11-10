from predictionClass import Predictions
from pprint import pprint

def test_handleAddEvent_validAddEvent():
    addEvent = {
        "attributes": {
            "bearing": 160.0,
            "current_status": "INCOMING_AT",
            "current_stop_sequence": 30,
            "direction_id": 0,
            "label": "3633-3868",
            "latitude": 42.36283874511719,
            "longitude": -71.05811309814453,
            "speed": None,
            "updated_at": "2018-06-08T11:22:55-04:00"
        },
        "id": "G-10300",
        "links": {
            "self": "/vehicles/G-10300"
        },
        "relationships": {
            "route": {
                "data": {
                    "id": "Green-E",
                    "type": "route"
                }
            },
            "stop": {
                "data": {
                    "id": "70204",
                    "type": "stop"
                }
            },
            "trip": {
                "data": {
                    "id": "36420357",
                    "type": "trip"
                }
            }
        },
        "type": "vehicle"
    }

    expectedPredictionMap = {
        "Green-E": {
            "place-haecl": {
                0: [
                    {
                        "attributes": {
                            "bearing": 160.0,
                            "current_status": "INCOMING_AT",
                            "current_stop_sequence": 30,
                            "direction_id": 0,
                            "label": "3633-3868",
                            "latitude": 42.36283874511719,
                            "longitude": -71.05811309814453,
                            "speed": None,
                            "updated_at": "2018-06-08T11:22:55-04:00"
                        },
                        "id": "G-10300",
                        "links": {
                            "self": "/vehicles/G-10300"
                        },
                        "relationships": {
                            "route": {
                                "data": {
                                    "id": "Green-E",
                                    "type": "route"
                                }
                            },
                            "stop": {
                                "data": {
                                    "id": "70204",
                                    "type": "stop"
                                }
                            },
                            "trip": {
                                "data": {
                                    "id": "36420357",
                                    "type": "trip"
                                }
                            }
                        },
                        "type": "vehicle"
                    },
                ]
            }
        }
    }

    predictions = Predictions()
    predictions.createStopIdMaps()
    predictions.handleAddEvent(addEvent)
    assert(expectedPredictionMap == predictions.data)
    
def test_handleUpdateEvent_validUpdateEvent():

    updateEvent = {
        "attributes": {
            "bearing": 76.0,
            "current_status": "IN_TRANSIT_TO",
            "current_stop_sequence": 8,
            "direction_id": 0,
            "label": "1633",
            "latitude": 42.56092834472656,
            "longitude": -70.81510162353516,
            "speed": 19.0,
            "updated_at": "2018-06-08T11:21:52-04:00"
        },
        "id": "1633",
        "links": {
            "self": "/vehicles/1633"
        },
        "relationships": {
            "route": {
                "data": {
                    "id": "CR-Newburyport",
                    "type": "route"
                }
            },
            "stop": {
                "data": {
                    "id": "Beverly Farms",
                    "type": "stop"
                }
            },
            "trip": {
                "data": {
                    "id": "CR-Weekday-Spring-18-107",
                    "type": "trip"
                }
            }
        },
        "type": "vehicle"
    }

    expectedPredictionMap = {
        "CR-Newburyport": {
            "place-GB-0229": {
                0: [
                    {
                        "attributes": {
                            "bearing": 76.0,
                            "current_status": "IN_TRANSIT_TO",
                            "current_stop_sequence": 8,
                            "direction_id": 0,
                            "label": "1633",
                            "latitude": 42.56092834472656,
                            "longitude": -70.81510162353516,
                            "speed": 19.0,
                            "updated_at": "2018-06-08T11:21:52-04:00"
                        },
                        "id": "1633",
                        "links": {
                            "self": "/vehicles/1633"
                        },
                        "relationships": {
                            "route": {
                                "data": {
                                    "id": "CR-Newburyport",
                                    "type": "route"
                                }
                            },
                            "stop": {
                                "data": {
                                    "id": "Beverly Farms",
                                    "type": "stop"
                                }
                            },
                            "trip": {
                                "data": {
                                    "id": "CR-Weekday-Spring-18-107",
                                    "type": "trip"
                                }
                            }
                        },
                        "type": "vehicle"
                    }
                ]
            }
        }
    }

    predictions = Predictions()
    predictions.createStopIdMaps()
    predictions.handleUpdateEvent(updateEvent)
    assert(expectedPredictionMap == predictions.data)


def test_handleUpdateEvent_validUpdateEventWithExistingData():

    updateEvent = {
        "attributes": {
            "bearing": 76.0,
            "current_status": "IN_TRANSIT_TO",
            "current_stop_sequence": 8,
            "direction_id": 0,
            "label": "1633",
            "latitude": 42.56092834472656,
            "longitude": -70.81510162353516,
            "speed": 19.0,
            "updated_at": "2018-06-08T11:21:52-04:00"
        },
        "id": "1633",
        "links": {
            "self": "/vehicles/1633"
        },
        "relationships": {
            "route": {
                "data": {
                    "id": "CR-Newburyport",
                    "type": "route"
                }
            },
            "stop": {
                "data": {
                    "id": "Beverly Farms",
                    "type": "stop"
                }
            },
            "trip": {
                "data": {
                    "id": "CR-Weekday-Spring-18-107",
                    "type": "trip"
                }
            }
        },
        "type": "vehicle"
    }

    existingPredictionMap = {
        "attributes": {
            "bearing": 76.0,
            "current_status": "IN_TRANSIT_TO",
            "current_stop_sequence": 8,
            "direction_id": 0,
            "label": "1633",
            "latitude": 10,
            "longitude": 10,
            "speed": 19.0,
            "updated_at": "2018-06-08T10:10:10-04:00"
        },
        "id": "1633",
        "links": {
            "self": "/vehicles/1633"
        },
        "relationships": {
            "route": {
                "data": {
                    "id": "CR-Newburyport",
                    "type": "route"
                }
            },
            "stop": {
                "data": {
                    "id": "Beverly Farms",
                    "type": "stop"
                }
            },
            "trip": {
                "data": {
                    "id": "CR-Weekday-Spring-18-107",
                    "type": "trip"
                }
            }
        },
        "type": "vehicle"
    }

    expectedPredictionMap = {
        "CR-Newburyport": {
            "place-GB-0229": {
                0: [
                    {
                        "attributes": {
                            "bearing": 76.0,
                            "current_status": "IN_TRANSIT_TO",
                            "current_stop_sequence": 8,
                            "direction_id": 0,
                            "label": "1633",
                            "latitude": 42.56092834472656,
                            "longitude": -70.81510162353516,
                            "speed": 19.0,
                            "updated_at": "2018-06-08T11:21:52-04:00"
                        },
                        "id": "1633",
                        "links": {
                            "self": "/vehicles/1633"
                        },
                        "relationships": {
                            "route": {
                                "data": {
                                    "id": "CR-Newburyport",
                                    "type": "route"
                                }
                            },
                            "stop": {
                                "data": {
                                    "id": "Beverly Farms",
                                    "type": "stop"
                                }
                            },
                            "trip": {
                                "data": {
                                    "id": "CR-Weekday-Spring-18-107",
                                    "type": "trip"
                                }
                            }
                        },
                        "type": "vehicle"
                    }
                ]
            }
        }
    }

    predictions = Predictions()
    predictions.createStopIdMaps()
    predictions.handleAddEvent(existingPredictionMap)
    predictions.handleUpdateEvent(updateEvent)
    pprint(expectedPredictionMap)
    pprint(predictions.data)
    assert(expectedPredictionMap == predictions.data)

