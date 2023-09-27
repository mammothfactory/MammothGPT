#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "MIT License"
__status__     = "Development
__deprecated__ = False
__version__    = "0.1.0"
"""

# Disable PyLint linting messages
# https://pypi.org/project/pylint/
# pylint: disable=line-too-long
# pylint: disable=invalid-name

# Standard Python libraries
import sqlite3

from datetime import datetime, time, timedelta 	# Manipulate calendar dates & time objects https://docs.python.org/3/library/datetime.html
from time import sleep
import pytz 					                # World Timezone Definitions  https://pypi.org/project/pytz/

import json                                     # Use to serialize a list of list and insert into TEXT column of SQLite database
from typing import Optional

# Internal modules
import GlobalConstants as GC

from ParcelId import ParcelId


class Database:
    
    DEBUGGING = True
    
    """ Store non-Personally Identifiable Information in SQLite database
    """

    def __init__(self, dbName='MammothGPT.db'):
        """ Constructor to initialize a MammothGPT Database object
            Call db = Database('Test.db') for testing
        
        Args:
            dbName (String): Filename of SQlite database, defaults to 'House.db'   
        """
        # Connect to the database (create if it doesn't exist)
        self.conn = sqlite3.connect(dbName)
        self.conn.execute("PRAGMA foreign_keys = ON")
        
        self.cursor = self.conn.cursor()

        # Create TODO tables in TimeReport.db for user name and time logging data storage
        # content (string), url (string), timestamp (datetime), dump (string), segment (string), image_urls (list of list [[string, string]])
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DataSetTable (id INTEGER PRIMARY KEY, content TEXT, url TEXT, timestamp TEXT, dump TEXT, segment TEXT, image_urls TEXT)''')
        
        qPublicQuery = (''' CREATE TABLE IF NOT EXISTS QPublicRecord (
                            id                  INTEGER     PRIMARY KEY,
                            urlPageID           INTEGER     NOT NULL,
                            owner_info_id       INTEGER     NOT NULL,
                            parcel_summary_id   INTEGER     NOT NULL,
                            FOREIGN KEY (owner_info_id)     REFERENCES OwnerInfoTable(id),
                            FOREIGN KEY (parcel_summary_id) REFERENCES ParcelSummaryTable(id)
                            )''')
        
        self.cursor.execute(qPublicQuery)
        
        # https://www.transportation.gov/sites/dot.gov/files/docs/mission/gis/national-address-database/308816/nad-schema-v1.pdf
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS OwnerInfoTable (id INTEGER PRIMARY KEY, contactName TEXT, streetAddress TEXT, city TEXT, county TEXT, state CHAR(2), postalCode INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ParcelSummaryTable (id INTEGER PRIMARY KEY, parcelId TEXT, parcelAddress TEXT, description TEXT, propertyUseCode TEXT, acreage REAL, homestead CHAR(1), link TEXT)''')
        #TODO self.cursor.execute('''CREATE TABLE IF NOT EXISTS SalesTable (id INTEGER PRIMARY KEY, saleDate TEXT, salePrice INTEGER, qualification CHAR(1),  vacant CHAR(1),  grantor TEXT,  grantee TEXT)''')
        #TODO self.cursor.execute('''CREATE TABLE IF NOT EXISTS ValuationTable (id INTEGER PRIMARY KEY, FOREIGN KEY working_values_id, FOREIGN KEY certified_values_id)''') 
        """
        WorkingValuesTable
                
        buildingValue INTEGER,
        extraFeatureValue INTEGER,
        landValue INTEGER,
        landAgriculturalValue INTEGER,
        
        
        """

        
        # Create debuging logg
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DebugLoggingTable (id INTEGER PRIMARY KEY, logMessage TEXT)''')
        
        # Commit the five tables to database
        self.conn.commit()
        
    
    def setup_tables(self):
        """ Define initial users for 
        """
        data = "Ruth’s Chris Steak House Concepts For Weight Management"
        exampleUrl = "https://canige-constancia.org/2020/ruths-chris-steak-house-concepts-for-weight-management/"
        exampleImageUrl= [["http://canige-constancia.org/wp-content/uploads/2020/07/images-1.jpg", "Best Restaurant"]]

        db.insert_dataset_table(data, exampleUrl, exampleImageUrl)


    def commit_changes(self):
        """ Commit data inserted into a table to the *.db database file 
        """
        self.conn.commit()


    def close_database(self):
        """ Close database to enable another sqlite3 instance to query a *.db database
        """
        self.conn.close()


    def get_date_time(self) -> str:
        """ Get date and time in Marianna, FL timezone, independent of location on server running code

        Returns:
            String: e.g. "2022-09-25T05:06:45 for current time
        """
        tz = pytz.timezone('America/Chicago')
        zulu = pytz.timezone('UTC')
        now = datetime.now(tz)
        if now.dst() == timedelta(0):
            now = datetime.now(zulu) - timedelta(hours=6)
            #print('Standard Time')

        else:
            now = datetime.now(zulu) - timedelta(hours=5)
            #print('Daylight Savings')   
            
        return now.isoformat(timespec="minutes")


    def query_table(self, tableName: str, row: Optional[int]= None, column: Optional[int]= None) -> tuple:
        """ Return every row of a table from a *.db database

        Args:
            tableName (String): Name of table in database to query

        Returns:
            result: A list of tuples from a table, where each row in table is a tuple of length n
            isEmpty: Returns True if table is empty, and False otherwise
            isValid: Returns True is table name exists in MammothGPT.db, and False otherwise
            
        """
        try:
            sqlStatement = f"SELECT * FROM {tableName}"
            self.cursor.execute(sqlStatement)

            isEmpty = False
            isValid = True
            result = self.cursor.fetchall()
            if len(result) == 0:
                isEmpty = True

      
            if row == None and column == None:
                return result, isEmpty, isValid
            elif column == None:
                return result[row-1], isEmpty, isValid
            else:
                if column == GC.IMAGE_URL_COLUMN_NUMBER:
                    return json.loads(result[row-1][column]), isEmpty, isValid
                else:
                    return result[row-1][column], isEmpty, isValid
                
        except IndexError:
            db.insert_debug_logging_table(f'Invalid table row or column number {row} OR {column} respectively was requested')
            return None, None, False
        
        except sqlite3.OperationalError:
            db.insert_debug_logging_table(f'The {tableName} table does NOT exist in MammothGPT.db or there is typo in table name')
            return None, None, False

    
    def insert_dataset_table(self, newContent: str, pageUrl: str, imageUrls: list):
        """ Insert TODO into DataSetTable of database
            Example data format at https://huggingface.co/datasets/tiiuae/falcon-refinedweb/viewer/default/train?p=9680000&row=968000000

        Args:
            newContent (str):
            pageUrl (str):
            imageUrl (list): [URL string for image at this pageUrl,  Alt-Text string for image at an imageUrl]
        """
        
        currentDateTime = self.get_date_time()
        
        jsonImageUrls = json.dumps(imageUrls)
        
        self.cursor.execute("INSERT INTO DataSetTable (content, url, timestamp, dump, segment, image_urls) VALUES (?, ?, ?, ?, ?, ?)", (newContent, pageUrl, currentDateTime, GC.TODO_DUMP, GC.TODO_REAL_ESTATE_SEGMENT, jsonImageUrls))
        self.commit_changes()
 
 
    def insert_owner_info_table(self, name: str, address: str, city: str, county: str, stateAbbrev: str, zipcode: int) -> int:
        city = city.title()                 # All words capitalized 
        county = county.title()             # All words capitalized 
        stateAbbrev = stateAbbrev.upper()   # All letters capitalized
        
        self.cursor.execute("INSERT INTO OwnerInfoTable (contactName, streetAddress, city, county, state, postalCode) VALUES (?, ?, ?, ?, ?, ?)", (name, address, city, county, stateAbbrev, zipcode))
        lastIdInserted = self.cursor.lastrowid
        self.commit_changes()   
        
        return lastIdInserted
    
    
    def insert_parcel_summary_table(self, id: str, adress: str, desc: str, useCode: str, totalAcreage: float, isHomestead: str, stateAbbrev: str, mapLink: str) -> int:
        isHomestead = isHomestead.upper()
        stateAbbrev = stateAbbrev.upper()
        
        #id = ParcelId(id, stateAbbrev)
        #id.searchString
        self.cursor.execute("INSERT INTO ParcelSummaryTable (parcelId, parcelAddress, description, propertyUseCode, acreage, homestead, link) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, adress, desc, useCode, totalAcreage, isHomestead, mapLink))
        lastIdInserted = self.cursor.lastrowid
        self.commit_changes()   
        
        return lastIdInserted

        
    def insert_q_public_table(self, pageId: int, owner_tableId: int, parcel_tableId: int) -> int:
        self.cursor.execute("INSERT INTO QPublicRecord (urlPageID, owner_info_id, parcel_summary_id) VALUES (?, ?, ?)", (pageId, owner_tableId, parcel_tableId))
        lastIdInserted = self.cursor.lastrowid
        self.commit_changes()   
        
        return lastIdInserted  


    def get_QPublicRecord(self, columnValue: int, columnName: str= "id") -> list:
        """ Get 

        Args:
            columnName (str): _description_
            columnValue (int): _description_

        Returns:
            list: Of All Tables stored as foreign key in QPublicRecord table
        """
        ownerQuery = "SELECT owner_info_id from QPublicRecord WHERE " + columnName + "=" + str(columnValue)
        parcelQuery = "SELECT parcel_summary_id from QPublicRecord WHERE " + columnName + "=" + str(columnValue)
        allSubTables = []
        
        try:
            ownerCursor = self.conn.execute(ownerQuery)
            parcelCursor = self.conn.execute(parcelQuery)
            
            for dataTuple in ownerCursor:
                ownerForeignKey = dataTuple[0]
    
            for dataTuple in parcelCursor:
                parcelForeignKey = dataTuple[0] 
                
            allSubTables.append(self.get_OwnerInfoTable(["*"], ownerForeignKey))
            allSubTables.append(self.get_ParcelSummaryTable(["*"], parcelForeignKey))
                
        except sqlite3.OperationalError:
            db.insert_debug_logging_table(f'The {columnName} column name does NOT exist')
            return []
        
        except UnboundLocalError:
            db.insert_debug_logging_table(f'The {columnName} column name does NOT contain a value = {columnValue}')
            return []
        
        return allSubTables
        
        
    def get_OwnerInfoTable(self, columnNames: list, id: int) -> tuple:
        """ Return specific columns of a PRIMARY KEY ID in the OwnerInfoTable

        Args:
            columnNames (list): Column data to return. Use * to get ALL columns
            id (int): PRIMARY KEY ID 

        Returns:
            tuple: TODO
        """
        columns = ','.join(columnNames)
        query = "SELECT " + columns + " from OwnerInfoTable WHERE id=" + str(id)
        
        try:
            cursor = self.conn.execute(query)
            for dataTuple in cursor: 
                return dataTuple
            
        except sqlite3.OperationalError:
            db.insert_debug_logging_table(f'At least one item in {columnNames} list does NOT exist in the OwnerInfoTable or has a typo')
            return ()


    def get_ParcelSummaryTable(self, columnNames: list, id: int) -> tuple:
        """ Return specific columns of a PRIMARY KEY ID in the ParcelSummaryTable

        Args:
            columnNames (list): Column data to return. Use * to get ALL columns
            id (int): PRIMARY KEY ID 

        Returns:
            tuple: TODO
        """
        columns = ','.join(columnNames)  
        query = "SELECT " + columns + " from ParcelSummaryTable WHERE id=" + str(id)
        
        try:
            cursor = self.conn.execute(query)
            for dataTuple in cursor: 
                return dataTuple
            
        except sqlite3.OperationalError:
            db.insert_debug_logging_table(f'At least one item in {columnNames} list does NOT exist in the ParcelSummaryTable or has a typo')
            return ()
        
    
    def insert_debug_logging_table(self, debugText: str):
        """ 

        Args:
            debugText (str): ERROR: or WARNING: text message to log 
        """
        self.cursor.execute("INSERT INTO DebugLoggingTable (logMessage) VALUES (?)", (debugText,))
        self.commit_changes()
        

    def search_dataset_table(self, searchTerm: str):
        """ Search Dataset table for every occurrence of a string

        Args:
            searchTerm (str): Strict string to search for

        Returns:
            List: Of Tuples from a DatasetTable, where each List item is a row in the table containing the exact search term
        """
        self.cursor.execute("SELECT * FROM DatasetTable WHERE content LIKE ?", ('%' + str(searchTerm) + '%',))
        results = self.cursor.fetchall()

        return results


    def TEST_1(db):
        """ db.query_table tests
        """    
        row = 1
        data, isEmpty, isValid = db.query_table("DataSetTable", row, GC.IMAGE_URL_COLUMN_NUMBER)
        print(data)
        
        row = 2
        data, isEmpty, isValid = db.query_table("DataSetTable", row, GC.IMAGE_URL_COLUMN_NUMBER)
        print(data)
        
        log, isEmpty, isValid = db.query_table("DebugLoggingTable")
        if isValid and isEmpty: 
            print("The DebugLoggingTable in MammothGPT.db is empty")
        else:
            print(log)

            
    def TEST_2(db):
        
        data = db.get_OwnerInfoTable(["contactName, city, county"], 1)
        print(data)
        
        ownerInfoForeignKey = db.insert_owner_info_table("Blaze Sanders", "2924 Green Street", "Marianna", "Jackson", "FL", 32446)
        data, isEmpty, isValid = db.query_table("OwnerInfoTable")
        print(data)
        
        parcelSummaryForeignKey = db.insert_parcel_summary_table("01-2N-10-0000-0020-0000", "RUN E 280 FT TO BEGIN, RUN E 280 FT, N 330 FT, W 280 FT, S 330 FT TO POB...INGRESS/ EGRESS...OR 1434 P 52 D.I.E...", "MOBILE HOME 0200", 4.92, "Y", "FL", "https://beacon.schneidercorp.com/Application.aspx?AppID=851&LayerID=15884&PageTypeID=1&PageID=7080&Q=57980097&KeyValue=01-2N-12-0373-00B0-0140")
        data, isEmpty, isValid = db.query_table("ParcelSummaryTable")
        print(data)    
        
        try:
            db.insert_q_public_table(19999, ownerInfoForeignKey, parcelSummaryForeignKey)
            db.insert_q_public_table(13353, 4, 4)
            
        except sqlite3.IntegrityError: 
            db.insert_debug_logging_table(f'Foreign Key 4 does NOT exists in OwnerInfoTable') 
    

if __name__ == "__main__":
    print("Testing MammothGPT Test.db using Database.py")

    db = Database('Test.db')
    primaryId = db.insert_q_public_table(12345, 1, 5)
    data = db.get_QPublicRecord(primaryId)
    print(data) 
    
    db.close_database()
    