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

        sql = ''' INSERT INTO users(user,password,nombre,sudo)
              VALUES(?,?,?,?) '''
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
            users[row[0]]=(row[1],row[3])
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
            return temp[0]
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
 
        if transaccion[5] is None:
            sql = ''' INSERT INTO transacciones(obra_id,responsable,rubro_id,valor,tipo)
              VALUES(?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, transaccion[0:5])
            return cur.lastrowid 
        else:
            sql = ''' INSERT INTO transacciones(obra_id,responsable,rubro_id,valor,tipo,cliente_id)
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
    
def select_transacciones_cliente(cliente_id):
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM transacciones WHERE cliente_id = ?"
        cur = conn.cursor()
        cur.execute(sql,cliente_id)
 
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

def get_rubro_by_nombre_obra(combo,completo=False):
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM rubros WHERE nombre = ? and tipo = ? and obra_id = ?"
        cur = conn.cursor()
        cur.execute(sql,combo)
 
        rows = cur.fetchall()
        if completo:
            return rows[0]
        else:
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
        
def update_nombre_rubro(presu,rubro):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = ''' UPDATE rubros
              SET nombre = ? 
              WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, (presu,rubro))
        conn.commit()
        
def delete_rubro(rubro):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = 'DELETE FROM transacciones WHERE rubro_id=?'
        cur = conn.cursor()
        cur.execute(sql, (rubro,))
        conn.commit()  
        sql = 'DELETE FROM rubros WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (rubro,))
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
 
        sql = ''' INSERT INTO rubros(obra_id,nombre,tipo,presupuesto,persistir)
              VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, rubro)
        return cur.lastrowid 
    
def get_aptos_obra(obra):
    database = "database/trialdb.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM obras WHERE id = ?"
        cur = conn.cursor()
        cur.execute(sql,obra)
 
        rows = cur.fetchall()
        return rows[0][9]

def create_contrato(contrato):
    database = "database/trialdb.db"
 
    # create a database connection
    
    conn = create_connection(database)
    with conn:
 
        sql = ''' INSERT INTO contratos(obra_id, responsable,cliente_id,saldo,
                                    numero_apto,tipo,fecha_ini)
              VALUES(?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, contrato)
        return cur.lastrowid 
   
def create_cuota(cuota):
    database = "database/trialdb.db"
 
    # create a database connection
    
    conn = create_connection(database)
    with conn:
 
        sql = ''' INSERT INTO cuotas(obra_id, contrato_id,cliente_id,valor,
                                    detalle,fecha,tipo,estado)
              VALUES(?,?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, cuota)
        return cur.lastrowid 

def descontar_apto(obra):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM obras WHERE id = ?"
        cur = conn.cursor()
        cur.execute(sql,obra)
 
        rows = cur.fetchall()
        temp = rows[0][9]       
        temp = temp-1
        
        sql = ''' UPDATE obras
              SET disponibles = ? 
              WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, (temp,obra[0]))
        conn.commit()
        
def actualizar_saldo(contrato):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM cuotas WHERE contrato_id = ?"
        cur = conn.cursor()
        cur.execute(sql,contrato)
 
        rows = cur.fetchall()
        total = 0
        for i in rows:
            if i[8] == 'Por Pagar':
                total += i[4]
                
        sql = ''' UPDATE contratos
              SET saldo = ? 
              WHERE id = ?'''
        cur = conn.cursor()
        dummy = (total,contrato[0])
        cur.execute(sql, dummy)
        conn.commit()
    
def get_tipocontrato_by_cuota(cuota):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM cuotas WHERE id = ?"
        cur = conn.cursor()
        cur.execute(sql,cuota)
 
        rows = cur.fetchall()
        elcontrato = rows[0][2]
        
        sql = "SELECT * FROM contratos WHERE id = ?"
        cur = conn.cursor()
        cur.execute(sql,(elcontrato,))
        rows = cur.fetchall()
        eltipo = rows[0][6]
        return eltipo
    
def cambiar_pagado(a_cambiar):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:       
                    
        sql = ''' UPDATE cuotas
              SET estado = 'Pagado' 
              WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, a_cambiar)
        conn.commit()
        
def get_cuotas_por_pagar():
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM cuotas WHERE estado = 'Por Pagar'"
        cur = conn.cursor()
        cur.execute(sql)
 
        rows = cur.fetchall()
        return rows
    
def get_cuota(elid):
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM cuotas WHERE id = ?"
        cur = conn.cursor()
        cur.execute(sql,(elid,))
        
        temp = cur.fetchall()
        if len(temp) > 0:
            return temp[0]
        else :
            return temp

def get_facturas_vencidas():
    database ="database/trialdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        sql = "SELECT * FROM cuotas"
        cur = conn.cursor()
        cur.execute(sql)
        
        temp = cur.fetchall()
        temp2 = []
        for i in temp:
            if i[8] == "Por Pagar":
                temp2.append(i)
        return temp2
    
def create_arky():
    arkyid = create_obra(('Arky','Bogotá','','','','','','','',''))
    create_rubro((arkyid,"Inversionistas","Entrada",0,1))
    create_rubro((arkyid,"Ventas","Entrada",0,1))
    create_rubro((arkyid,"Préstamos","Entrada",0,1))
    create_rubro((arkyid,"Retorno Inversionistas","Después",0,1))
    create_rubro((arkyid,"Retorno Prestamistas","Después",0,1))
    
    