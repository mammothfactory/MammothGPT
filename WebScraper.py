#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "Collect data from the TODO and TODO websites"
"""


import requests
from bs4 import BeautifulSoup

# Internal modules
from Database import Database

baseURLs = ["https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html", "https://realpython.github.io/fake-jobs/"]

FLORIDA_COUNTIES =  ["Alachua": , "Baker", "Bay", "Bradford", "Brevard", "Broward", "Calhoun", "Charlotte", "Citrus", "Clay", "Collier", "Columbia",
                    "DeSoto", "Dixie", "Duval", "Escambia", "Flagler", "Franklin", "Gadsden", "Gilchrist", "Glades", "Gulf",
                    "Hamilton", "Hardee", "Hendry", "Hernando", "Highlands", "Hillsborough", "Holmes", "Indian River",
                    "Jackson", "Jefferson", "Lafayette", "Lake", "Lee", "Leon", "Levy", "Liberty",
                    "Madison", "Manatee", "Marion", "Martin", "Miami-Dade" : "https://www.miamidade.gov/pa/online_tools.asp", "Monroe", "Nassau",
                    "Okaloosa", "Okeechobee", "Orange", "Osceola", "Palm Beach", "Pasco", "Pinellas", "Polk", "Putnam",
                    "Santa Rosa", "Sarasota", "Seminole", "St. Johns", "St. Lucie", "Sumter", "Suwannee",
                    "Taylor", "Union", "Volusia", "Wakulla", "Walton", "Washington"]

# https://www.miamidade.gov/pa/property_folio_numbers.asp
# https://www.propertyshark.com/mason/fl/Jackson-County/Maps
# https://www.qpublic.net/ == https://beacon.schneidercorp.com

# Folio Number equals ???




class WebScraper:
    """ Create a six column table in SQlite to build a Hugging Face DataSet for Falcon LLM https://huggingface.co/datasets/tiiuae/falcon-refinedweb/viewer/default/train?p=9680000
        content (string), url (string), timestamp (datetime), dump (string), segment (string), image_urls (sequence)
        
    """
    
if __name__ == "__main__":
    page = requests.get(baseURLs[1])
    print(page.text)
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    results = soup.find(id="ResultsContainer")
    #print(results.prettify())
    
    job_elements = results.find_all("div", class_="card-content")
    for job_element in job_elements:
        title_element = job_element.find("h2", class_="title")
        company_element = job_element.find("h3", class_="company")
        location_element = job_element.find("p", class_="location")
        print(title_element.text.strip())
        print(company_element.text.strip())
        print(location_element.text.strip())
        print()
        
    
