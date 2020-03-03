# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 00:09:55 2020

@author: Ditto Castform
"""


import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
 
 
if __name__ == '__main__':
    create_connection("database/trialdb.db")