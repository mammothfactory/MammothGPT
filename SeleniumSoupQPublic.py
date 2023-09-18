from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
from time import sleep

import requests
from bs4 import BeautifulSoup

import GlobalConstants as GC

def construct_beacon_schneidercorp_url(parcelId: str) -> str:
    """ Construct a valid url to return valid HTML from 
        Example URL = https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353&Q=1070396039&KeyValue=01-2N-12-0223-0010-0010

    Args:
        stateZipCode (int): 5 digit state zip code
        landUseCodeActivity (list): See https://support.regrid.com/parcel-data/lbcs-keys

    Returns:
        str: Valid URL with multiple & parameters after ?
    """
    url = "https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353&Q=1070396039" + "&KeyValue=" + str(parcelId) 
    return url


# Create a new Safari session
driver = webdriver.Safari()

url = construct_beacon_schneidercorp_url("01-2N-12-0373-00B0-0140")    #01-2N-12-0223-0010-0011 is an INVALID Parcel ID
driver.get(url)

# Wait for Javascript to fully render the HTML
driver.implicitly_wait(5)
renderedHtml = driver.page_source

soup = BeautifulSoup(renderedHtml, 'html.parser') 

container = soup.find("main", id="maincontent")
#print(container)

owner_name = None
owner_address = None
try:
    owner_element = container.find("div", class_="sdw1-owners-ownerspace")
    #print(owner_element)
    owner_name = soup.find("span", {"id": "ctlBodyPane_ctl01_ctl01_rptOwner_ctl00_sprOwnerName1_lnkUpmSearchLinkSuppressed_lblSearch"}).text
    owner_address = soup.find("span", {"id": "ctlBodyPane_ctl01_ctl01_rptOwner_ctl00_lblOwnerAddress"}).get_text(separator=" ", strip=True)
    
    parcel_summary_element = container.find("table", class_="tabular-data-two-column")
    second_column_contents = [td.get_text(strip=True) for td in soup.select("table.tabular-data-two-column td")]
    #print(second_column_contents)
    parcel_id = second_column_contents[GC.PARCEL_ID_ROW]
    parcel_address = second_column_contents[GC.PARCEL_ADDRESS_ROW]     
    parcel_description = second_column_contents[2]
    parcel_property_use_code = second_column_contents[3]
    parcel_acreage = second_column_contents[7]
    parcel_is_homestead = second_column_contents[8]
    
    parcel_summary_map_element = container.find("table", id="ctlBodyPane_ctl02_ctl01_tbMapLink")
    link = parcel_summary_map_element.find("a href")
    #print(parcel_summary_map_element)
    print(link)
    
    #self.cursor.execute('''CREATE TABLE IF NOT EXISTS ParcelSummaryTable (id INTEGER PRIMARY KEY, parcelId TEXT, description TEXT, propertyUseCode TEXT, acreage REAL, homestead CHAR(1))''')
    
except AttributeError:
    print("ERROR: Invalid URL and/or Parcel ID = {}")
    
finally:
    print(f'Owner Name: {owner_name}')
    print(f'Owner Address: {owner_address}')

#element = driver.find_element(By.ID, "stateMenuButton")
#print(element)
#sleep(30)

driver.quit()
