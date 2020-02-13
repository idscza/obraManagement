# -*- coding: utf-8 -*-
"""

Clase de datos falsos para entrega 1

@author: Ditto Castform
"""

import random as r

def generate_mockup(nombre):
    
    mud = {"nombre":nombre}
    
    mud['Entradas'] = {}
    mud['Entradas']['Inversionistas'] = r.randint(10,100)*1000000
    mud['Entradas']['Ventas'] = r.randint(10,100)*1000000
    
    salidas = {}
    salidas['Retorno Inversionistas'] =  r.randint(10,100)*1000000
    salidas['Nomina Empresarial'] =  r.randint(10,100)*1000000
    salidas['Retorno Inversionistas'] =  r.randint(10,100)*1000000
    salidas['Stuff'] =  r.randint(10,100)*1000000
    salidas['Stuff1'] =  r.randint(10,100)*1000000
    salidas['Ejecución Proyectos'] =  r.randint(10,100)*1000000
    
    
    mud['Salidas'] = salidas
    
    return mud
