import pprint
import requests
import urllib.parse
import datetime

API_KEY="43a45acc39ad4b2cb73936d6fd8f047a"
MBTA_API_ENDPOINT="https://api-v3.mbta.com/"

firstPath = "predictions/?filter[stop]=North+Station&filter[route]=CR-Lowell&filter[direction_id]=0&include=schedule"
firstRequest= MBTA_API_ENDPOINT + firstPath
firstRequestHeader={
    "X-API-Key": API_KEY
}    
northStation=urllib.parse.unquote_plus("North+Station")
firstRequestParams={
    "filter[stop]": northStation,
    "filter[route]": "CR-Lowell",
    "filter[direction_id]": "0",
    "include": "schedule",
}

firstResponse = requests.get(
    MBTA_API_ENDPOINT + "predictions/",
    headers=firstRequestHeader,
    params=firstRequestParams
)

# firstResponse = requests.get(MBTA_API_ENDPOINT + firstPath)

print(firstResponse.status_code)
#print(firstResponse.headers)
#print(firstResponse.request.url)

#pprint.pprint(firstResponse.json())
departureTime = firstResponse.json()["included"][0]["attributes"]["departure_time"]
departureTime = datetime.datetime.fromisoformat(departureTime)
departureTime = departureTime.time()
print(departureTime.strftime("%I:%M %p"))
