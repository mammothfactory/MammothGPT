#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "CONSTANTS for Llama2 and Falcon MammothGPT LLM's"
"""

# Disable PyLint linting messages
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name

TODO = -1 

PRIMARY_KEY_COLUMN_NUMBER = 0
CONTECT_COLUMN_NUMBER = 1
URL_COLUMN_NUMBER = 2
TIMESTAMP_COLUMN_NUMBER = 3
DUMP_COLUMN_NUMBER = 4
SEGMENT_COLUMN_NUMBER = 5
IMAGE_URL_COLUMN_NUMBER = 6

INSERT_SUCCESSFUL = 200
INSERT_FAILED = 400

TODO_REAL_ESTATE_SEGMENT = "1664030334514.38"
TODO_DUMP = "CC-MAIN-2023-40"

# https://regrid.com/api CONSTANTS
PARCEL_URL = "https://app.regrid.com/api/v1/search.json"

# Florida CONSTANTS
FLORIDA_COUNTIES =  ["Alachua", "Baker", "Bay", "Bradford", "Brevard", "Broward", "Calhoun", "Charlotte", "Citrus", "Clay", "Collier", "Columbia",
                    "DeSoto", "Dixie", "Duval", "Escambia", "Flagler", "Franklin", "Gadsden", "Gilchrist", "Glades", "Gulf",
                    "Hamilton", "Hardee", "Hendry", "Hernando", "Highlands", "Hillsborough", "Holmes", "Indian River",
                    "Jackson", "Jefferson", "Lafayette", "Lake", "Lee", "Leon", "Levy", "Liberty",
                    "Madison", "Manatee", "Marion", "Martin", "Miami-Dade", "Monroe", "Nassau",
                    "Okaloosa", "Okeechobee", "Orange", "Osceola", "Palm Beach", "Pasco", "Pinellas", "Polk", "Putnam",
                    "Santa Rosa", "Sarasota", "Seminole", "St. Johns", "St. Lucie", "Sumter", "Suwannee",
                    "Taylor", "Union", "Volusia", "Wakulla", "Walton", "Washington"]

COUNTY_PROPERTY_WEBSITES = {}

https://www.qpublic.net/fl/jackson/search.html

https://beacon.schneidercorp.com

# Florida & Jackson          https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=2&PageID=7081
# Florida & Jefferson County https://beacon.schneidercorp.com/Application.aspx?AppID=866&LayerID=16381&PageTypeID=2&PageID=7226

# The folllowing two are equal when searching for 01-2N-10-0000-0020-0020
https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353&Q=435552219&KeyValue=01-2N-10-0000-0020-0020
https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353&KeyValue=01-2N-10-0000-0020-0020

# If a parcel ID does not exist like 01-2N-10-0000-0010-0001  
#https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=3&PageID=7082&Q=1127906194
