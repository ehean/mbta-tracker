import requests
import pprint
import constants
import argparse


resp = requests.get(
    constants.MBTA_API_ENDPOINT + "stops",
    headers=constants.REQUEST_HEADER
)

if resp.status_code == 200:
    file = open("stops.py", "w")
    file.write("STOPS_MAP={")
    resp = resp.json()
    for resource in resp["data"]:
        file.write("\"" + resource["attributes"]["name"] + "\": \"" + resource["id"] + "\"\n")
    file.write("}")
    file.close()
    print("Success")
else:
    resp = resp.json()
    pprint.pprint(resp)
    raise Exception("Did not receive 200 status code.")
