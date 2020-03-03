# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 00:11:55 2020

@author: Ditto Castform
"""

import sqlite3
from sqlite3 import Error
import sqlAccess as sql


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

 
 
def main():
    database = "database/trialdb.db"
 
    crear_usuarios = """ CREATE TABLE IF NOT EXISTS users (
                                        user text PRIMARY KEY,
                                        password text NOT NULL,
                                        nombre text NOT NULL
                                    ); """
 
    crear_obras = """CREATE TABLE IF NOT EXISTS obras (
                                    id integer PRIMARY KEY,
                                    nombre text NOT NULL,
                                    ciudad text NOT NULL,
                                    direccion text NOT NULL,
                                    encargado text NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL                       
                                );"""
    
    crear_transacciones = """CREATE TABLE IF NOT EXISTS transacciones (
                                    id integer PRIMARY KEY,
                                    obra_id integer NOT NULL,
                                    responsable text NOT NULL,
                                    rubro text NOT NULL,
                                    valor real NOT NULL,
                                    tipo text NOT NULL,
                                    presupuestado text NOT NULL,
                                    FOREIGN KEY (obra_id) REFERENCES obras (id),
                                    FOREIGN KEY (responsable) REFERENCES users (user)
                                );"""
 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        # create users
        create_table(conn, crear_usuarios)
 
        # create obras
        create_table(conn, crear_obras)
        
        # create transacciones
        #create_table(conn, crear_transacciones)
        create_table(conn, crear_transacciones)
    else:
        print("Error! cannot create the database connection.")
    
    sql.create_user("admin","admin","Administrador")
        
main()