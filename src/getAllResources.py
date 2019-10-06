import requests
import pprint
import constants
import argparse

def argumentParser():
    argParser = argparse.ArgumentParser("This Python script returns the all IDs for a given MBTA resource.")
    argParser.add_argument("-r", "--resource", help="Resource name (e.g. stop, route)", action="store")
    args = argParser.parse_args()
    return args

args = argumentParser()

resp = requests.get(
    constants.MBTA_API_ENDPOINT + args.resource,
    headers=constants.REQUEST_HEADER,
    params={ "fields": "id" }
)

if resp.status_code == 200:
    file = open(args.resource + "_list.txt", "w")
    resp = resp.json()
    for resource in resp["data"]:
        file.write("\"" + resource["attributes"]["name"] + "\": " + resource["id"] + "\"\n")
    print("Success")
else:
    resp = resp.json()
    pprint.pprint(resp)
    raise Exception("Did not receive 200 status code.")
