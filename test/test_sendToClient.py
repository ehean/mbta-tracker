import pytest
import sendToClient
import datetime
import constants

# Unit test naming convention:
#   [MethodName_StateUnderTest_ExpectedBehavior]

def test_getSecondsAwayFromDateTime_NullObject_ReturnNull():
    assert sendToClient.getSecondsAwayFromDateTime(None) == None

def test_getDisplayValueFromAttribute_NullObect_ReturnNull():
    assert sendToClient.getDisplayValueFromAttribute(None) == ""

def test_getDisplayValueFromAttribute_HasStatus_ReturnStatus():
    attribute = {
        "status": "STATUS"
    }

    assert sendToClient.getDisplayValueFromAttribute(attribute) == attribute["status"]

def test_getDisplayValueFromAttribute_NoStatusAndOnlyArrivalIsAvailable_ReturnArrival():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus120Sec = now + datetime.timedelta(0,120)
    nowPlus120SecIsoFormat = nowPlus120Sec.isoformat()
    attribute = {
        "status": None,
        "arrival_time": nowPlus120SecIsoFormat
    }

    assert sendToClient.getDisplayValueFromAttribute(attribute) == "2 minutes"

def test_getDisplayValueFromAttribute_NoStatusAndArrivaAndDeparturelIsAvailable_ReturnArrival():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus120Sec = now + datetime.timedelta(0,120)
    nowPlus240Sec = now + datetime.timedelta(0,240)
    nowPlus120SecIsoFormat = nowPlus120Sec.isoformat()
    nowPlus240SecIsoFormat = nowPlus240Sec.isoformat()
    attribute = {
        "status": None,
        "arrival_time": nowPlus120SecIsoFormat,
        "departure_time": nowPlus240SecIsoFormat
    }

    assert sendToClient.getDisplayValueFromAttribute(attribute) == "2 minutes"


def test_getDisplayValueFromAttribute_NoStatusAndOnlyDepartureIsAvailable_ReturnDeparture():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus120Sec = now + datetime.timedelta(0,120)
    nowPlus120SecIsoFormat = nowPlus120Sec.isoformat()
    attribute = {
        "status": None,
        "departure_time": nowPlus120SecIsoFormat
    }

    assert sendToClient.getDisplayValueFromAttribute(attribute) == "2 minutes"

def test_getDisplayValueFromAttribute_StatusIsSTOPPED_ATAndArrivalIsLessThanOrEqualTo90Sec_ReturnBoarding():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus90Sec = now + datetime.timedelta(0,90)
    nowPlus90SecIsoFormat = nowPlus90Sec.isoformat()
    attribute = {
        "status": "STOPPED_AT",
        "arrival_time": nowPlus90SecIsoFormat
    }

    assert sendToClient.getDisplayValueFromAttribute(attribute) == "Boarding"

def test_getDisplayValueFromAttribute_StatusIsSTOPPED_ATAndArrivalIsGreaterThan90Sec_ReturnStoppedAt():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus91Sec = now + datetime.timedelta(0,91)
    nowPlus91SecIsoFormat = nowPlus91Sec.isoformat()
    attribute = {
        "status": "STOPPED_AT",
        "arrival_time": nowPlus91SecIsoFormat
    }

    assert sendToClient.getDisplayValueFromAttribute(attribute) == "STOPPED_AT"

def test_getDisplayValueFromAttribute_NoStatusAndOnlyArrivalisLessThanOrEqualTo30Sec_ReturnArriving():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus30Sec = now + datetime.timedelta(0,30)
    nowPlus30SecIsoFormat = nowPlus30Sec.isoformat()
    attribute = {
        "status": None,
        "arrival_time": nowPlus30SecIsoFormat
    }

    assert sendToClient.getDisplayValueFromAttribute(attribute) == "Arriving"

def test_getDisplayValueFromAttribute_NoStatusAndOnlyArrivalisLessThanOrEqualTo60Sec_ReturnApproaching():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus60Sec = now + datetime.timedelta(0,60)
    nowPlus60SecIsoFormat = nowPlus60Sec.isoformat()
    attribute = {
        "status": None,
        "arrival_time": nowPlus60SecIsoFormat
    }

    assert sendToClient.getDisplayValueFromAttribute(attribute) == "Approaching"

def test_getDisplayValueFromAttribute_NoStatusAndOnlyArrivalisLessThanOrEqualTo89Sec_Return1Min():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus89Sec = now + datetime.timedelta(0,89)
    nowPlus89SecIsoFormat = nowPlus89Sec.isoformat()
    attribute = {
        "status": None,
        "arrival_time": nowPlus89SecIsoFormat
    }

    assert sendToClient.getDisplayValueFromAttribute(attribute) == "1 minute"

def test_getPredictedTimeFromAttribute_ArrivalTimeAndDepartureTimePresent_ReturnArrivalTime():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus120Sec = now + datetime.timedelta(0,120)
    nowPlus240Sec = now + datetime.timedelta(0,240)
    nowPlus120SecIsoFormat = nowPlus120Sec.isoformat()
    nowPlus240SecIsoFormat = nowPlus240Sec.isoformat()
    attribute = {
        "status": None,
        "arrival_time": nowPlus120SecIsoFormat,
        "departure_time": nowPlus240SecIsoFormat
    }

    assert sendToClient.getPredictedTimeFromAttribute(attribute) == nowPlus120Sec

def test_getPredictedTimeFromAttribute_ArrivalTimePresent_ReturnArrivalTime():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus120Sec = now + datetime.timedelta(0,120)
    nowPlus120SecIsoFormat = nowPlus120Sec.isoformat()
    attribute = {
        "status": None,
        "arrival_time": nowPlus120SecIsoFormat
    }

    assert sendToClient.getPredictedTimeFromAttribute(attribute) == nowPlus120Sec

def test_getPredictedTimeFromAttribute_DepartureTimePresent_ReturnDepartureTime():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus240Sec = now + datetime.timedelta(0,240)
    nowPlus240SecIsoFormat = nowPlus240Sec.isoformat()
    attribute = {
        "status": None,
        "departure_time": nowPlus240SecIsoFormat
    }

    assert sendToClient.getPredictedTimeFromAttribute(attribute) == nowPlus240Sec

def test_getSecondsAwayFromDateTime_DatetimeIs60SecAway_Return60():
    now = datetime.datetime.now()
    now = now.replace(tzinfo=constants.UTC_ZONE)
    now = now.astimezone(constants.EST_ZONE)
    nowPlus60Sec = now + datetime.timedelta(0,60)
    
    assert round(sendToClient.getSecondsAwayFromDateTime(nowPlus60Sec)) == 60
    
