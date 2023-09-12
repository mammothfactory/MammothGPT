class ParcelId:

    def __init__(self, parcelId: str, state: str) -> None:
        """ Create folio/tax/parcel number 
        https://www.revenue.alabama.gov/faqs/what-is-the-parcel-identification-number/#:~:text=This%2016%20digit%20number%20uniquely,31%2D3%2D004%2D019.003
        https://www.encyclopedia.com/articles/how-to-find-a-property-parcel-number/

        Args:
            parcelId (str): Example: 16-09-31-3-004-019.003
        """
        
        if state.capitalize() == "Florida":
            result = parcelId.split("-")
            self.locator = result[0]
            self.area = result[1]
            self.section = result[2]
            self.quarterSection = result[3]
            self.block = result[4]
            
            tmp = result[5].split(".")  
            self.parcel = tmp[0]   
            self.subparcel = tmp[1]
        else:
            self.locator = None
            self.area = None
            self.section = None 
            self.quarterSection = None
            self.block = None
            self.parcel = None
            self.subparcel = None
        
        
if __name__ == "__main__":
    
    home = ParcelId("16-09-31-3-004-019.003", "Florida")
    work = ParcelId("16-09-31-3-004-019.003", "Texas")
    print(home.locator)
    print(work.locator)
    
"""
Alabama
Alaska
Arizona
Arkansas
California
Colorado
Connecticut
Delaware
Florida
Georgia
Hawaii
Idaho
Illinois
Indiana
Iowa
Kansas
Kentucky
Louisiana
Maine
Maryland
Massachusetts
Michigan
Minnesota
Mississippi
Missouri
Montana
Nebraska
Nevada
New Hampshire
New Jersey
New Mexico
New York
North Carolina
North Dakota
Ohio
Oklahoma
Oregon
Pennsylvania
Rhode Island
South Carolina
South Dakota
Tennessee
Texas
Utah
Vermont
Virginia
Washington
West Virginia
Wisconsin
Wyoming
"""