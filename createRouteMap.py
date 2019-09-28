import requests
import pprint
import constants
import argparse

routesResp = requests.get(
    constants.MBTA_API_ENDPOINT + "routes",
    headers=constants.REQUEST_HEADER
)

if routesResp.status_code == 200:
    file = open("routesMap.py", "w")
    file.write("ROUTES_MAP={\n")
    routesResp = routesResp.json()
    for route in routesResp["data"]:
    
        file.write("\t\"" + route["id"] + "\": {\n") 
        
        stopsResp = requests.get(
            constants.MBTA_API_ENDPOINT + "stops",
            headers=constants.REQUEST_HEADER,
            params={"filter[route]": route["id"]}
        )
        
        if stopsResp.status_code == 200:
            stopsResp = stopsResp.json()
            for stop in stopsResp["data"]:
                file.write("\t\t\"" + stop["attributes"]["name"] + "\": \"" + stop["id"] + "\",\n")
        else:
            resp = resp.json()
            pprint.pprint(resp)
            raise Exception("Did not receive 200 status code.")
        file.write("\t},\n")
else:
    resp = resp.json()
    pprint.pprint(resp)
    raise Exception("Did not receive 200 status code.")

file.write("}\n")
file.close()
print("Success")

