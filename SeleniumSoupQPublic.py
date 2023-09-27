from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.by import By
from time import sleep
import random

# Using the Jackson County Property Appraiser's office info what are the standard acreage sizes?
What county in Florida has the lowest tax rate?
What property type in Holmes County is selling quickest?
What is the average cost of single-family home in Holmes County, Florida?
import requests
from bs4 import BeautifulSoup

import GlobalConstants as GC

from ParcelId import ParcelId
from Database import Database


def construct_beacon_schneidercorp_url(rawParcelId: str) -> str:
    """ Construct a valid url to request valid HTML from 
        Example URL = https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353&Q=1070396039&KeyValue=01-2N-12-0223-0010-0010
        With the unneeded &Q=1070396039& parameter removed

    Args:
        rawParcelId (str): Unsanitized user input with possible characters such as '-' or '.'

    Returns:
        str: Valid URL with multiple parameters (&) after the separator (?)
    """
    url = "https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353" + "&KeyValue=" + str(rawParcelId) 
    return url


def parse_raw_owner_address(firstOwner: str, inputText: str) -> tuple:
    """ Parse raw strings scraped from https://beacon.schneidercorp.com/ HTML text into a format for database insertion 

    Args:
        firstOwner (str): Unsanitized name from https://beacon.schneidercorp.com which contains an '&' character if property has 2nd owner 
        inputText (str):  Unsanitized address from https://beacon.schneidercorp.com which may conatin 2nd owner name

    Returns:
        tuple: (allOwners, streetAddress, city, state, postalCode, error) where error is True is any value can't be determined
    """
    error = False
    
    if firstOwner == '' and inputText == '':
        # URL was invalid since BOTH function inputs where empty 
        error = True
        return  None, None, None, None, None, error     
    
    lines = inputText.split("\n")
    #print(f'Adddress Lines = {lines}')
    secondOwner = ''
    streetAddress = ''
    city_state_postal = ['', '']                # Standard data would be ['Marianna', 'FL 32446']
    state = ''
    
    try:
        indexErrorCheck = lines[3]              # indexErrorCheck is '' or DOES NOT EXIST because of final \n  character in inputText function parameter
        
        secondOwner = lines[0].strip()
        streetAddress = lines[1].strip()
        city_state_postal = lines[2].split(',')

    except IndexError:
       streetAddress = lines[0].strip()
       city_state_postal = lines[1].split(',')
    
    finally:
        try:
            city = city_state_postal[0].strip()
            state_postal = city_state_postal[1].strip().split('  ')   # NOTE: TWO EMPTY SPACES!!!
            state = state_postal[0].strip().upper()
            postalCode = state_postal[1].strip()
            
            if state == '' or postalCode == '':
                error = True
                
        except IndexError:
            error = True
        
        allOwners = (firstOwner + " " + secondOwner).strip()
    
    return allOwners, streetAddress, city, state, postalCode, error


def parse_raw_parcel_summary(parcel_id: str, address: str, description: str, use_code: str, parcel_acreage: float, is_homestead: str, mapLink: str):
    error = False
    """
    ['01-3N-07-0000-0310-0011', '1604  GULF POWER RDSneads', 
     'OR 183 P 453   OR 500 P 753 OR 519 P 993   OR 797 P 901 OR 833 P 12   OR 1350 P 640 COMM AT SWC OF SE1/4 OF SECT TO BEGIN, RUN N ALONG E/LY RTWY OF CNTY RD #271  364.57 FT, N 88* E 429.82 FT, S 371.04 FT TO S/LY LINE OF SE1/4 OF SECT, W 423.97 FT TO POB... OR 1367 P 475  OR 1729 P 32  LESS 1 AC PER OR 1735 P 952(Note: *The Description above is not to be used on legal documents.)', 
     'VACANT 0000(Note: *The Use Code is a Dept. of Revenue (DOR) code. For zoning information, please contact the Jackson County Community Development office at (850) 482-9637. For zoning information within aCITY/TOWN, please contact thatCITY/TOWNhall.)', 
     '01-3N-07', '15', '12.378', '2.6', 'N']
    """
    parcelId = parcel_id
    parcelAddress = address    # Some counties add city name to the end of street address
    desc = description
    useCode = None
    acreage = None
    isHomestead = None
    link = None
    
    try:
        code_note = use_code.split(sep='(')
        useCode = "Department of Revenue (DOR) Code: " + code_note[0]
    except IndexError:
        error = True
    
    if parcel_acreage == '':
        error = True
    else:
        acreage = float(parcel_acreage)
    
    if not (len(is_homestead) == 1):
        error = True
    else:
        isHomestead = is_homestead
    
    if mapLink == '':
        error = True
    else:
        link = mapLink

    return (parcelId, parcelAddress, desc, useCode, acreage, isHomestead, link, error)


def next_parcel_id(rawParcelId: str) -> str:
    
    currentId = ParcelId(rawParcelId)
    nextId = currentId.next()
    
    return nextId


if __name__ == "__main__":
    # Create a new Safari session
    #driver = webdriver.Safari()
    db = Database('ScrapeGPT.db')
    id = ParcelId("01-2N-10-0000-000F-0100", "FL")
    JACKSON_COUNTY_SECTION_TOWNSHIP_RANGE_BLOCK_PARCEL_SUBPARCEL_MIN = ['01', '2N', '10', '0000', '0000', '0000']
    JACKSON_COUNTY_SECTION_TOWNSHIP_RANGE_BLOCK_PARCEL_SUBPARCEL_MAX = ['36', '7N', '14', '0100', '01FF', '0100']
    
    """ 
    https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353&Q=662899328&KeyValue=01-2N-12-0373-00B0-0140    # Base case
    https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353&Q=662899328&KeyValue=01-2N-12-0223-0010-0011    # INVALID Parcel ID
    https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353&Q=2127686832&KeyValue=01-2N-10-0000-0030-0011   # One owner
    https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=4&PageID=13353&Q=594701655&KeyValue=01-3N-07-0000-0310-0011    
    """
    validUrl = True
    for i in range(5_518_800_001):
        driver = webdriver.Safari()
        nextId = id.next(JACKSON_COUNTY_SECTION_TOWNSHIP_RANGE_BLOCK_PARCEL_SUBPARCEL_MIN, JACKSON_COUNTY_SECTION_TOWNSHIP_RANGE_BLOCK_PARCEL_SUBPARCEL_MAX)
        print(f"URL to search is: {nextId}")
        url = construct_beacon_schneidercorp_url(nextId)
        #url = construct_beacon_schneidercorp_url("01-2N-12-0373-00B0-0140")
        driver.get(url)

        # Wait for Javascript to fully render the HTML
        driver.implicitly_wait(3)
        renderedHtml = driver.page_source

        soup = BeautifulSoup(renderedHtml, 'html.parser') 

        owner_name = ''
        owner_address = None
        county = ''
        parcel_id = ''
        parcel_address = ''
        parcel_description = '' 
        parcel_property_use_code = '' 
        parcel_acreage = ''
        parcel_is_homestead = '' 
        state = ''
        mapLink = ''
        
        try:
            banner = soup.find("h1", id="ctlHeader_hAppName")
            county = banner.text.split(',')[0].strip()
            #print(county)
            
            container = soup.find("main", id="maincontent")
            #print(container)
            
            owner_element = container.find("div", class_="sdw1-owners-ownerspace")
            #print(owner_element)
            
            # The order of these next two statements matter. 
            # The HTML tag used for owner_address variable will ALWAYS throw an AttributeError if URL in driver.get(url) is INVALID
            # The owner_name HTML tag can throw AttributeError for many reasons, and is thus not a good tag to base program branching on 
            # Strip=False keeps "\n" for parsing in  parse_long_owner_address() function. 
            owner_address = owner_element.find("span", {"id": "ctlBodyPane_ctl01_ctl01_rptOwner_ctl00_lblOwnerAddress"}).get_text(separator=" ", strip=False)    
            owner_name = owner_element.find("span", {"id": "ctlBodyPane_ctl01_ctl01_rptOwner_ctl00_sprOwnerName1_lnkUpmSearchLinkSuppressed_lblSearch"}).text
            
        except AttributeError:
            if owner_address == None:
                owner_address = ''
                owner_name = ''
                db.insert_debug_logging_table(f'ERROR: Invalid URL and/or Parcel ID = {url} at {db.get_date_time()}')
                validUrl = False
            else:
                owner_name = owner_element.find("a", {"id": "ctlBodyPane_ctl01_ctl01_rptOwner_ctl00_sprOwnerName1_lnkUpmSearchLinkSuppressed_lnkSearch"}).text
            
        finally:
            if validUrl:
                parcel_summary_element = container.find("table", class_="tabular-data-two-column")
                second_column_contents = [td.get_text(strip=True) for td in soup.select("table.tabular-data-two-column td")]
                #print(second_column_contents)
                parcel_id = second_column_contents[GC.PARCEL_ID_ROW]
                parcel_address = second_column_contents[GC.PARCEL_ADDRESS_ROW]
                parcel_description = second_column_contents[GC.PARCEL_DESC_ROW]
                parcel_property_use_code = second_column_contents[GC.PARCEL_USE_CODE_ROW]
                parcel_acreage = second_column_contents[GC.PARCEL_ACREAGE_ROW]
                parcel_is_homestead = second_column_contents[GC.PARCEL_IS_HOMESTEAD_ROW]

                parcel_summary_map_element = container.find("table", id="ctlBodyPane_ctl02_ctl01_tbMapLink")
                href_value = parcel_summary_map_element.find("a", {"id": "ctlBodyPane_ctl02_ctl01_lnkMap"})["href"]
                mapLink = "https://beacon.schneidercorp.com/" + href_value
                #print(f'Map Link:  {link}')
            
                
                #print(f'Owner Name: {owner_name}')
                #print(f'Owner Address: {owner_address}')
            
                (allOwners, streetAddress, city, state, postalCode, ownerError) = parse_raw_owner_address(owner_name, owner_address)
                (parcelId, parcelAddress, desc, useCode, acreage, isHomestead, link, summaryError) = parse_raw_parcel_summary(parcel_id, parcel_address, parcel_description, parcel_property_use_code, parcel_acreage, parcel_is_homestead, mapLink)
                print(f'Parcel ID scraped was: {parcelId}')
            
                if not ownerError and not summaryError:
                    #print(county)
                    db.insert_owner_info_table(allOwners, streetAddress, city, county, state, postalCode)
                    db.insert_parcel_summary_table(parcelId, parcelAddress, desc, useCode, acreage, isHomestead, state, link)
                    
                else:
                    db.insert_debug_logging_table(f'Parsing of address data -{owner_address}- failed at {db.get_date_time()}')
                
        id = ParcelId(nextId, "FL")
        validUrl = True
        sleep(random.uniform(3, 6))
        driver.quit()
