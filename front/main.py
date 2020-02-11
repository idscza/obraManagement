# -*- coding: utf-8 -*-
"""

Esqueleto de programa de manejo de presupuesto de obras

@author: Ditto Castform
"""

from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
import mockupdata as mu
from functools import partial

def __main__():
    window = Tk()
    window.title("Manejo de Presupuesto")
    window.geometry('1050x550')



    lbl = Label(window, text="Bienvenidos al Manejador \nde Presupuestos de Obras",font=("Arial",20))
    lbl.grid(column=0, row=1)

    lbl1 = Label(window, text='\n\n')
    lbl1.grid(column=1,row=0)
    
    txt = scrolledtext.ScrolledText(window,width=70,height=10)
    txt.grid(column=1, row=1)
    
    btn = Button(window, text="Agregar Obra")
    btn.grid(column=0, row=2)
      
     
    combo = Combobox(window)
    forz_act = partial(actualizar_valores,[combo,txt])
    window.bind('<<ComboboxSelected>>', forz_act)
    cheat = partial(cargar_obras,combo)
    combo.grid(column = 0, row = 3)
    
    menus = Menu(window)
 
    new_item = Menu(menus)

    
    new_item.add_command(label='Cargar Obras',command=cheat)
    new_item.add_command(label='Seleccionar Obra')
    
    menus.add_cascade(label='Obras', menu=new_item)
    window.config(menu=menus) 
    
    window.mainloop()

#Totally Mockup, it should call SQL DB
def cargar_obras(combob):
    combob['values'] = ('Los Alpes','Real Danés','Atalayas')
    combob.current(0)
    
def actualizar_obras(combob,val):
    tup = combob['values']
    tupact = []
    for i in tup:
        tupact.add(i)
    tupact.add(val)
    tupact = tuple(tupact)
    combob['values'] = tupact

def actualizar_valores(data,x):
    name = data[0].get()
    texto = data[1]
    corpus = ''
    
    corpus = name
    
    texto.delete(1.0,END)
    texto.insert(INSERT,corpus)
    #texto.update_idletasks()


__main__()