# -*- coding: utf-8 -*-
"""

Clase de datos falsos para entrega 1

@author: Ditto Castform
"""

import random as r

def generate_mockup(nombre):
    
    mud = {"nombre":nombre}
    mud["prep1"] = r.randint(10,100)*1000000
    
    return mud
