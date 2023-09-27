import re

import GlobalConstants as GC

class InvalidParcelIdError(Exception):
    def __init__(self, message):
        super().__init__(message)   
        
class MaxParcelIdError(Exception):
    def __init__(self, message):
        super().__init__(message)   

class ParcelId:

    def __init__(self, parcelId: str, state: str) -> None:
        """ Create folio/tax/parcel number 
        https://www.revenue.alabama.gov/faqs/what-is-the-parcel-identification-number/#:~:text=This%2016%20digit%20number%20uniquely,31%2D3%2D004%2D019.003
        https://www.encyclopedia.com/articles/how-to-find-a-property-parcel-number/

        Args:
            parcelId (str): Example: 16-09-31-3-004-019.003
            state (str): State abbreviation 
        """
        if state.upper() == "FL":
            result = parcelId.split("-")
            self.section = result[0]
            self.township = result[1]
            self.range = result[2]
            self.block = result[3]
            self.parcel = result[4]
            self.subparcel = result[5]
            self.numOfComponents = 6
            
            if len(result[0]) > 2 or len(result[1]) > 3 or len(result[2]) > 2 or len(result[3]) > 4 or len(result[4]) > 4 or len(result[5]) > 4:
                raise InvalidParcelIdError(f"Please check the length of each component of the new Parcel ID: {parcelId}") 
                
            self.searchString = self.remove_non_alphanumeric_characters(parcelId)
        
        elif state.upper() == "AL":
            result = parcelId.split("-")
            self.locator = result[0]
            self.area = result[1]
            self.section = result[2]
            self.quarterSection = result[3]
            self.block = result[4]
            
            tmp = result[5].split(".")  
            self.parcel = tmp[0] 
            try:  
                self.subparcel = tmp[1]
            except IndexError:
                self.subparcel = None
            
            self.searchString = self.remove_non_alphanumeric_characters(parcelId)
            
        else:
            self.locator = None
            self.area = None
            self.section = None 
            self.quarterSection = None
            self.block = None
            self.parcel = None
            self.subparcel = None
            self.searchString = None
    
    
    def remove_non_alphanumeric_characters(self, rawString) -> str:
        """ Pattern matches any character that's not a letter (uppercase or lowercase) or a number and replace with empty string, effectively removing them

        Args:
            rawString (_type_): Input strinf 

        Returns:
            str: With only letter A to Z (or a to Z) and 0 to 9
        """
        return re.sub(r'[^a-zA-Z0-9]', '', rawString)
    

    def add_leading_zero_if_needed(number: str, FORMAT: GC) -> str | None:
        """ Add upto 3 leading zeros to any decimal or hexadecimal under 

        Args:
            number (str): 
            FORMAT (GC): Global Constant defining the format on the input string number

        Returns:
            str | None: _description_
        """
        try:
            if (len(number) > 4 and FORMAT == GC.DECIMAL) or len(number) > 6 and FORMAT == GC.HEXADECIMAL:
                return '0000'
            
            if FORMAT == GC.DECIMAL:
                if int(number) < 10000:
                    return f"{int(number):04d}"
                else:
                    return str(number)
        
            elif FORMAT == GC.HEXADECIMAL:
                hexNumber = int(number, 16)
                if hexNumber < 10000:
                    return f"{hexNumber:04X}"
                else:
                    return str(number)
            else:
                print("ERROR: Number format is not valid {FORMAT}")
                
        except ValueError:
            print("WARNING: One of the function number characters didn't match the function input FORMAT (0 to F): {number}")
            return None


    def next(self, minRange, maxRange) -> str:
        # https://web.gccaz.edu/~lynrw95071/Township%20Range%20Explanation.html
        # https://www.randymajors.org/map-images/Florida-Section-Township-Range-Map.png
        
        newSubparcel, newParcel, newBlock, newRange, newTownship, newSection = '', '', '', '', '', ''

        tempSubparcel = int(self.subparcel, 10) + 1
        if tempSubparcel <= int(maxRange[5]):
            newSubparcel = ParcelId.add_leading_zero_if_needed(str(tempSubparcel), GC.DECIMAL)
        else:
            newSubparcel = '0000'
        
        if int(self.subparcel) >= int(maxRange[5]):
            tempParcel = int(self.parcel, 16) + 1
            if tempParcel <= int(maxRange[4], 16):
                newParcel = ParcelId.add_leading_zero_if_needed(str(hex(tempParcel)), GC.HEXADECIMAL)
            else:
                newParcel = '0000'
        else:
            newParcel = self.parcel
            return (self.section + '-' +  self.township + '-' +  self.range + '-' + self.block + '-' + newParcel + '-' +  newSubparcel)
        
        
        if int(self.parcel, 16) >= int(maxRange[4], 16):
            tempBlock = int(self.block, 10) + 1
            if tempBlock <= int(maxRange[3]):
                newBlock = ParcelId.add_leading_zero_if_needed(str(tempBlock), GC.DECIMAL)
            else:
                newBlock = '0000'
        else:
            newBlock = self.block
            return (self.section + '-' +  self.township + '-' +  self.range + '-' + newBlock + '-' + newParcel + '-' +  newSubparcel)
        
        if int(self.block) >= int(maxRange[3]):
            tempRange = int(self.range, 10) + 1
            if tempRange <= int(maxRange[2]):
                newRange = ParcelId.add_leading_zero_if_needed(str(tempRange), GC.DECIMAL)[2:4]
            else:
                newRange = '00'
        else:
            newRange = self.range
            return (self.section + '-' +  self.township + '-' +  newRange + '-' + newBlock + '-' + newParcel + '-' +  newSubparcel)


        compassDirection = maxRange[1][1]
        if int(self.range) >= int(maxRange[2]):
            tempTownship = int(self.township.strip(compassDirection), 10) + 1
            if tempTownship <= int(maxRange[1].strip(compassDirection)):
                newTownship = ParcelId.add_leading_zero_if_needed(str(tempTownship), GC.DECIMAL)[2:4]
                newTownship = str(int(newTownship.split(compassDirection)[0])) + compassDirection
            else:
                newTownship = minRange[1]
        else:
            newTownship = self.township
            return (self.section + '-' +  newTownship + '-' +  newRange + '-' + newBlock + '-' + newParcel + '-' +  newSubparcel)
        
        
        if int(self.township.strip(compassDirection)) >= int(maxRange[1].strip(compassDirection)):
            tempSection = int(self.section, 10) + 1
            if tempSection <= int(maxRange[0]):
                newSection = ParcelId.add_leading_zero_if_needed(str(tempSection), GC.DECIMAL)[2:4]
            else:
                raise MaxParcelIdError(f"Overflow of all {self.numOfComponents} ParcelId componments ") 

        else:
            newSection = self.section
            

            
        return (newSection + '-' + newTownship + '-' +  newRange + '-' +  newBlock + '-' + newParcel + '-' +  newSubparcel)
        
        
if __name__ == "__main__":
    
    JACKSON_COUNTY_SECTION_TOWNSHIP_RANGE_BLOCK_PARCEL_SUBPARCEL_MIN = ['01', '2N', '07', '0000', '0000', '0000']
    JACKSON_COUNTY_SECTION_TOWNSHIP_RANGE_BLOCK_PARCEL_SUBPARCEL_MAX = ['36', '7N', '14', '0900', '0FFF', '0900']
    
    #FLORIDA_NORTH_MIN = TODO
    #FLORIDA_NORTH_MAX = TODO
    
    #FLORIDA_SOUTH_MIN = TODO
    #FLORIDA_SOUTH_MAX = TODO
    
    #work = ParcelId("16-09-31-3-004-00A.003", "TX")
    #print(work.searchString)
    #print(work.locator)
    
    #print(GC.STATES["FL"])
    
    output = ParcelId.add_leading_zero_if_needed('00A0', GC.HEXADECIMAL)
    #print(output)
    home = ParcelId("14-3N-14-0420-0FFE-0900", "FL")
    
    try:
        nextId = home.next(JACKSON_COUNTY_SECTION_TOWNSHIP_RANGE_BLOCK_PARCEL_SUBPARCEL_MIN, JACKSON_COUNTY_SECTION_TOWNSHIP_RANGE_BLOCK_PARCEL_SUBPARCEL_MAX)
        print(f"Does {home.searchString} + 1 = {nextId}")
    except MaxParcelIdError:
        print("Looping through all Parcel ID's is complete")
    
    
""" Open AI 
In the Florida Parcel ID "01-2N-12-0373-00B0-0140," the subsections have the following meanings:

- "01": This refers to the county or municipality within Florida. Each county or municipality has a unique numerical code assigned to it.
- "2N": This indicates the township range. In the United States Public Land Survey System, townships are six-mile by six-mile squares, and the "N" signifies "north" in this case.
- "12": This represents the section number within the township. A township is further divided into 36 sections, each measuring one square mile.
- "0373": This identifies the parcel or lot number within the section. It helps to differentiate individual properties within a particular section.
- "00B0": This is the subdivision or plat number assigned to the property within the section. It indicates a specific subdivision or plat where the property is located.
- "0140": This is the block number within the subdivision or plat. Many subdivisions are further divided into blocks, and this number helps to identify the block where the property is situated.

Understanding these subsections helps real estate agents, property assessors, and title researchers to accurately locate, identify, and refer to specific parcels of land within Florida's survey grid system.

Section: 01
The section is a subdivision of a township, and there are usually 36 sections in a standard township, numbered 1 through 36.
Township: 2N
The township represents a specific area of land, and it is typically identified by a number and a direction (N for North, S for South). The number indicates the township's position relative to a baseline, and the direction indicates whether it's north or south of that baseline.
Range: 12
The range represents another specific area of land, typically identified by a number. Like the township, this number indicates the range's position relative to a principal meridian, but there's no direction associated with a range.
Subdivision Code: 0373
This could refer to a specific plat or map of subdivided plots within the aforementioned section, township, and range.
Block: 00B0
Within the subdivision, this identifies a specific block or area.
Lot: 0140
Within a block, this identifies a specific lot or parcel.



"""