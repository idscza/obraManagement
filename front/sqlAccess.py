# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 21:56:28 2020

@author: Ditto Castform
"""

import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
 
def create_user(user):
    
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:

        sql = ''' INSERT INTO users(user,password,nombre)
              VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, user)
        return cur.lastrowid

def select_all_users():
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
 
        rows = cur.fetchall()
        
        users = {}
        for row in rows:
            users[row[0]]=row[1]
        return users

def get_name_by_user(username):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT nombre FROM users WHERE user = ?"
        cur = conn.cursor()
        cur.execute(sql,(username,))
        
        return cur.fetchall()[0][0]
 
def create_obra(obra):
    database = "database/trialdb.db"
 
    # create a database connection
    
    conn = create_connection(database)
    with conn:
 
        sql = ''' INSERT INTO obras(nombre,ciudad,direccion,encargado,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, obra)
        return cur.lastrowid

def select_all_obras():
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM obras")
 
        rows = cur.fetchall()
        
        users = []
        for row in rows:
            users.append(str(row[0]) + ". " +row[1])
        return tuple(users)

def create_transaccion(transaccion):
    database = "database/trialdb.db"
 
    # create a database connection
    
    conn = create_connection(database)
    with conn:
 
        sql = ''' INSERT INTO transacciones(obra_id,responsable,rubro,valor,tipo,presupuestado)
              VALUES(?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, transaccion)
        return cur.lastrowid 

        
def select_transacciones_obra(obra_id):
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM transacciones WHERE obra_id = ?"
        cur = conn.cursor()
        cur.execute(sql,obra_id)
 
        rows = cur.fetchall()
        
        return rows
    
def get_rubros_obra(obra_id):
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM transacciones WHERE obra_id = ?"
        cur = conn.cursor()
        cur.execute(sql,obra_id)
 
        rows = cur.fetchall()
        
        rta = []
        for row in rows:
            if row[5] == "Entrada":
                rta.append("Entrada: "+row[3])
            else:
                rta.append("Salida: "+row[3])
        rta = set(rta)
        rta = tuple(rta)
        return rta
    