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


class Database:
    
    DEBUGGING = True
    
    """ Store non-Personally Identifiable Information in SQLite database
    """

    def __init__(self):
        """ Constructor to initialize an Database object
        """
        # Connect to the database (create if it doesn't exist)
        self.conn = sqlite3.connect('MammothGPT.db')
        self.cursor = self.conn.cursor()

        # Create TODO tables in TimeReport.db for user name and time logging data storage
        # content (string), url (string), timestamp (datetime), dump (string), segment (string), image_urls (list of list [[string, string]])
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DataSetTable (id INTEGER PRIMARY KEY, content TEXT, url TEXT, timestamp TEXT, dump TEXT, segment TEXT, image_urls TEXT)''')
        
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


if __name__ == "__main__":
    print("Testing MammothGPT.db using Database.py")

    db = Database()
    
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

    db.close_database()
    