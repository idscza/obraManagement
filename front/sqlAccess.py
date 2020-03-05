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
    
def update_nuser(username,newname):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = ''' UPDATE users
              SET nombre = ? 
              WHERE user = ?'''
        cur = conn.cursor()
        cur.execute(sql, (newname,username))
        conn.commit()
        
def update_puser(username,newpw):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = ''' UPDATE users
              SET password = ? 
              WHERE user = ?'''
        cur = conn.cursor()
        cur.execute(sql, (newpw,username))
        conn.commit()
 
def create_obra(obra):
    database = "database/trialdb.db"
 
    # create a database connection
    
    conn = create_connection(database)
    with conn:
 
        sql = ''' INSERT INTO obras(nombre,ciudad,direccion,
        encargado,begin_date,end_date,
        cer_lib,licencia,disponibles,info_extra)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
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
    
def get_obra(elid):
    database ="database/trialdb.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM obras WHERE id = ?"
        cur = conn.cursor()
        cur.execute(sql,(elid,))
        
       
        temp = cur.fetchall()
        if len(temp) > 0:
            return temp[0]
        else :
            return temp
        
def get_cliente(elid):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM clientes WHERE documento = ?"
        cur = conn.cursor()
        cur.execute(sql,(elid,))
        
        temp = cur.fetchall()
        if len(temp) > 0:
            return cur.fetchall()[0]
        else :
            return temp

def select_all_clientes():
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM clientes")
 
        rows = cur.fetchall()
        
        clts = []
        for row in rows:
            clts.append([row[0],row[1],row[2]])
        return clts

def create_cliente(user):
    
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:

        sql = ''' INSERT INTO clientes(nombre,tipo_documento,
                documento,correo,telefono,direccion)
              VALUES(?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, user)
        return cur.lastrowid


def create_transaccion(transaccion):
    database = "database/trialdb.db"
 
    # create a database connection
    
    conn = create_connection(database)
    with conn:
 
        sql = ''' INSERT INTO transacciones(obra_id,responsable,rubro_id,valor,tipo)
              VALUES(?,?,?,?,?) '''
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
    
def select_rubros_obra(obra_id):
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM rubros WHERE obra_id = ?"
        cur = conn.cursor()
        cur.execute(sql,obra_id)
 
        rows = cur.fetchall()
        
        return rows
    
def get_rubros_obra(obra_id):
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM rubros WHERE obra_id = ?"
        cur = conn.cursor()
        cur.execute(sql,obra_id)
 
        rows = cur.fetchall()
        
        rta = []
        for row in rows:
            if row[3] == "Entrada":
                rta.append("Entrada: "+row[2])
            else:
                rta.append("Salida/"+row[3]+": "+row[2])
        rta = set(rta)
        rta = tuple(rta)
        return rta

def get_rubro_by_nombre_obra(combo):
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM rubros WHERE nombre = ? and obra_id = ?"
        cur = conn.cursor()
        cur.execute(sql,combo)
 
        rows = cur.fetchall()
        return rows[0][0]

def get_nombre_rubro(eid):
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM rubros WHERE id = ?"
        cur = conn.cursor()
        cur.execute(sql,eid)
 
        rows = cur.fetchall()
        return rows[0][2]
    
def update_presupuesto_rubro(presu,rubro):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = ''' UPDATE rubros
              SET presupuesto = ? 
              WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, (presu,rubro))
        conn.commit()

def update_obra(combo):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = ' UPDATE obras SET '+ combo[0]+'= ? WHERE id = ?'
        cur = conn.cursor()
        combofinal = combo[1],combo[2]
        cur.execute(sql, combofinal)
        conn.commit()
        
def create_rubro(rubro):
    database = "database/trialdb.db"
 
    # create a database connection
    
    conn = create_connection(database)
    with conn:
 
        sql = ''' INSERT INTO rubros(obra_id,nombre,tipo,presupuesto)
              VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, rubro)
        return cur.lastrowid 
   