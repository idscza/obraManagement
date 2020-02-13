# -*- coding: utf-8 -*-
"""

Clase de datos falsos para entrega 1

@author: Ditto Castform
"""
import random as r

mockups = ''

def generate_mockups(tupla):
    
    mus = []
    
    for nombre in tupla:
        mud = {"nombre":nombre}
    
        mud['Entradas'] = {}
        mud['Entradas']['Inversionistas'] = r.randint(1000,10000)*1000000
        mud['Entradas']['Ventas'] = r.randint(1000,10000)*1000000
    
        salidas = {}
        salidas['Retorno Inversionistas'] =  [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        salidas['Nomina Empresarial'] =  [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        salidas['Retorno Inversionistas'] =  [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        salidas['Obra: Limpieza de Lote'] =  [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        salidas['Obra: Insumos'] =  [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        salidas['Obra: Alquiler Maquinaria'] =  [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        salidas['Escrituras'] = [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        salidas['Permiso IDU'] = [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        salidas['Acabados: Cerámica'] = [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        salidas['Acabados: Electrodomésticos'] = [r.randint(10,100)*1000000,r.randint(5,10)*1000000]
        mud['Salidas'] = salidas
        mus.append(mud)
    
    global mockups
    mockups = mus

def get_mockup(nombre):
    
    global mockups
    elmu = ''
    for mu in mockups:
        if  mu['nombre'] ==  nombre:
            elmu = mu
    if elmu == '':
        huw = generate_new_mockup(nombre)
        mockups.append(huw)
        elmu = huw
    return elmu

def generate_new_mockup(nombre):
    
    mud = {"nombre":nombre}
    
    mud['Entradas'] = {}
    mud['Entradas']['Inversionistas'] = 0
    mud['Entradas']['Ventas'] = 0
    
    salidas = {}
    salidas['Retorno Inversionistas'] = [0,0]
    salidas['Nomina Empresarial'] =  [0,0]
    salidas['Retorno Inversionistas'] = [0,0]
    salidas['Obra: Limpieza de Lote'] = [0,0]
    salidas['Obra: Insumos'] = [0,0]
    salidas['Obra: Alquiler Maquinaria'] = [0,0]
    salidas['Escrituras'] = [0,0]
    salidas['Permiso IDU'] = [0,0]
    salidas['Acabados: Cerámica'] = [0,0]
    salidas['Acabados: Electrodomésticos'] = [0,0]
    mud['Salidas'] = salidas
    
    return  mud

def registrar_transaccion(nombre,transaccion,monto):
    eqe = ''
    for i in mockups:
        if i['nombre']==nombre:
            eqe = i
            break
    if eqe == '':
        return (False,'Obra no encontrada')
    try:
        monto = monto.replace(' ','')
        if monto == '':
            return (False,'Ingrese un valor en la transacción')
        monto = int(monto)
        if transaccion in eqe['Entradas'].keys():
            eqe['Entradas'][transaccion]+=monto
            return (True,'')
        elif transaccion in eqe['Salidas'].keys():
            if eqe['Salidas'][transaccion][0]==0:
                eqe['Salidas'][transaccion][0]=monto
                return (True,'')
            elif eqe['Salidas'][transaccion][1] + monto > eqe['Salidas'][transaccion][0]:
                return (False,'Esta transacción excede el presupuesto del rubro')
            elif fallo_de_presupuesto(eqe,monto):
                return (False,'Esta transacción excede el dinero disponible de la obra')
            else:
                eqe['Salidas'][transaccion][1] += monto
                return (True,'')
        else:
            return (False,'Transaccion no válida')
    except:
        return(False,'Ingrese por favor un número')

def fallo_de_presupuesto(obra,extra):
    loquentra = 0
    for i in obra['Entradas']:
        loquentra+=obra['Entradas'][i]
    loquehalasido = 0
    for j in obra['Salidas']:
        loquehalasido+=obra['Salidas'][j][1]
    loquehalasido+=extra
    if loquentra >loquehalasido:
        return False
    else:
        return True

def agregar_rubro(nombre,rubro,valor):
    eqe = ''
    for i in mockups:
        if i['nombre']==nombre:
            eqe = i
            break
    if eqe == '':
        return (False,'Obra no encontrada')
    try:
        valor = valor.replace(' ','')
        if valor == '':
            valor = 0
        valor = int(valor)
        rubro = rubro.strip()
        if rubro in eqe['Salidas'].keys():
            return (False,'Ya existe este rubro')
        else:
            eqe['Salidas'][rubro] = [valor,0]
            return(True,'')
    except:
       return(False,'Ingrese por favor un número')