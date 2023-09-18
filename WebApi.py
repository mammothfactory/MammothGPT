#from fastapi import FastAPI, HTTPException
import json
from uszipcode import SearchEngine
from typing import List, Tuple
from collections import deque
from Database import Database
import requests

# Load environment variables for usernames, passwords, & API keys
# https://pypi.org/project/python-dotenv/
from dotenv import dotenv_values

REGRID_DATA_SCHEMA_INVALID = "Too few or too many target keys found JSON returned by schema defined at https://support.regrid.com/parcel-data/schema"  

config = dotenv_values()
token = config['PARCEL_TRIAL_TOKEN']

HEADERS = {
    "accept": "application/json",
    "x-regrid-token": token
}

def count_key_occurence(filename: str, target_key: str) -> tuple:
    with open(filename, 'r') as f:
        data = json.load(f)

    count: int = 0
    queue = deque([data])

    while queue:
        current = queue.popleft()

        if isinstance(current, dict):
            for key, value in current.items():
                if key == target_key:
                    count += 1
                if isinstance(value, (dict, list)):
                    queue.append(value)
        elif isinstance(current, list):
            for item in current:
                if isinstance(item, (dict, list)):
                    queue.append(item)

    # Every real estate listing have two parcelnumb_no_formatting keys. One with the value and one with the descrtiption 
    if count % 2 == 0:
        numOfProperties = int(count / 2)
        return numOfProperties, None
    else:    
        return None, REGRID_DATA_SCHEMA_INVALID


def get_property_details(filename: str, desiredDetails: List[str]) -> tuple:
    """ 
        Every JSON response from ReGrid API has duplicate of every key, one with the value (int, float, or string )and one with a descrtiption (string)

    Args:
        filename (str): JSON file created from a json.dump() of a http requests.get()
        desiredDetails (List[str]): ReGrid Scheme keys to return as a List

    Returns:
        tuple: (value, error) where value is a List of Dictionarys, and error in 
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    
    queue = deque([data])
    outputDict = {}
    outputList = []
    i = 0
    
    while queue:
        current = queue.popleft()
        if isinstance(current, dict):
            for key, value in current.items():
                if key in desiredDetails:
                    outputDict[key] = value              # print(f'The Key-Value pair is {key} : {value}')
                    i += 1
                    if i % 2 == 0 and i > 0:
                        outputList.append(outputDict)
                        outputDict = {}
 
                if isinstance(value, (dict, list)):
                    queue.append(value)
                    
        elif isinstance(current, list):
            for item in current:
                if isinstance(item, (dict, list)):
                    queue.append(item)

    # Return every other dictionary inside the outputList List
    if len(outputDict) % 2 == 0:
        result = outputList[::2]
        return result, None
    else:
        return None, REGRID_DATA_SCHEMA_INVALID

    
def construct_regrid_url(stateZipCode: int, landUseCodeActivity: list) -> str:
    """ Construct a valid url to return valid JSON for Sample Use Case: szip, lbcs_activity and state2 at 
        https://developer.regrid.com/reference/get_api-v1-query-fields-szip-eq-46202-fields-lbcs-activity-between-2000-2999-fields-state2-eq-in-1
        Sample Demo URL = https://app.regrid.com/api/v1/query?fields[szip][eq]=46202&fields[lbcs_activity][between]=[2000,2999]&fields[state2][eq]=IN&context=%2Fus%2Fin%2Fmarion
        TODO Full Paid API URL = https://app.regrid.com/api/v1/query?fields[szip][eq]=55019&fields[lbcs_activity][between]=[1000,9500]&fields[state2][eq]=WI

    Args:
        stateZipCode (int): 5 digit state zip code
        landUseCodeActivity (list): See https://support.regrid.com/parcel-data/lbcs-keys

    Returns:
        str: Valid URL with multiple & parameters after ?
    """
    search = SearchEngine()
    result = search.by_zipcode(stateZipCode)
    state = result.state
    fullCountyName = str(result.county)
    county = fullCountyName.split()[0].lower()
    
    url = "https://app.regrid.com/api/v1/query?" + "fields[szip][eq]=" + str(stateZipCode) + "&fields[lbcs_activity][between]=" + str(landUseCodeActivity) + "&fields[state2][eq]=" + str(state) + "&context=%2Fus%2F" + str(state) + "%2F" + str(county) 
    return url
    





url =  construct_regrid_url(46202, [2000, 2100]) 
response = requests.get(url, headers=HEADERS)

if response.status_code == 200 and 'application/json' in response.headers['Content-Type']:
    data = response.json()
    with open("output.json", "w") as file:
        json.dump(data, file, indent=2)
else:
    print(f"Failed to fetch or parse JSON. Status code: {response.status_code}")

target_key = "parcelnumb_no_formatting"
print(count_key_occurence("output.json", target_key))


print(get_property_details("output.json", ["parcelnumb_no_formatting", "owner"]))


"""
#  Clark County, Wisconsin in in both ReGrid and qPublic
# 44.72895482703419, -90.62062781792035

# https://github.com/mammothfactory/mammoth_backend/blob/main/parcelapi/views.py
# https://regrid.com/api

# https://app.regrid.com/store/us/fl/jackson

# https://www.mapbox.com

# https://support.regrid.com/api/parcel-api-endpoints
# https://support.regrid.com/api/parcel-api-search#place-paths-for-context-narrow-searches-by-area
# https://support.regrid.com/parcel-data/schema


# https://developer.regrid.com/reference/get_api-v1-query-fields-szip-eq-46202-fields-lbcs-activity-between-2000-2999-fields-state2-eq-in-1
# https://support.regrid.com/parcel-data/lbcs-keys



""" 