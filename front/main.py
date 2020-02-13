# -*- coding: utf-8 -*-
"""

Esqueleto de programa de manejo de presupuesto de obras

@author: Ditto Castform
"""

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import *
import mockupdata as mu
from functools import partial

actual = {}
def_values = ('Los Alpes','Real Danés','Atalayas')

def __main__():
    window = Tk()
    window.title("Manejo de Presupuesto")
    window.geometry('915x270')



    lbl = Label(window, text="Bienvenidos al Manejador \nde Presupuestos de Obras",font=("Arial",20))
    lbl.grid(column=0, row=1)

    lbl1 = Label(window, text=' ')
    lbl1.grid(column=1,row=0)
    
    txt = scrolledtext.ScrolledText(window,width=70,height=10)
    txt.grid(column=1, row=1)
    
    btn1 = Button(window, text="Registrar Transacción")
    btn1.grid(column=1, row=2)
    
    btn2 = Button(window, text="Ver reporte")
    btn2.grid(column=1, row=3)
     
    combo = Combobox(window,width=32)
    forz_act = partial(actualizar_valores,[combo,txt])
    window.bind('<<ComboboxSelected>>', forz_act)

    combo.grid(column = 0, row = 3, sticky = (E))
    
    lbl2 = Label(window, text='       Obras\n     Actuales')
    lbl2.grid(column = 0, row = 3, sticky = (W))
    
    
    nomobra = Entry(window,width=35,state='disabled')
    nomobra.grid(column=0, row=2, sticky = (E))
    
    agob=partial(agregar_obra,[combo,txt,nomobra])
    btn = Button(window, text="Agregar\n  Obra",command=agob,state='disabled')
    btn.grid(column=0, row=2, sticky = (W))
    
    
    menus = Menu(window)
 
    new_item = Menu(menus)

    cheat = partial(cargar_obras,[combo,txt,btn,nomobra])   
    new_item.add_command(label='Cargar Obras',command=cheat)
    #new_item.add_command(label='Seleccionar Obra')
    
    menus.add_cascade(label='Obras', menu=new_item)
    
    
    
    window.config(menu=menus) 
    
    window.mainloop()

#Totally Mockup, it should call SQL DB
def cargar_obras(data):
    global def_values
    data[0]['values'] = def_values
    data[0].current(0)
    data[2].state(['!disabled'])
    data[3].state(['!disabled'])
    actualizar_valores(data,'')
'''    
def actualizar_obras(combob,val):
    tup = combob['values']
    tupact = []
    for i in tup:
        tupact.add(i)
    tupact.add(val)
    tupact = tuple(tupact)
    combob['values'] = tupact
    '''

def actualizar_valores(data,x):
    name = data[0].get()
    texto = data[1]
    corpus = ''
    
    corpus = name
    mud = mu.generate_mockup(name)
    
    global actual
    actual = mud
    
    mud1 = {'Entradas':mud['Entradas'],
            'Salidas':mud['Salidas']}
    
    corpus+='\n'
    for val in mud1:
        corpus+= '\n'
        dummy = mud1[val]
        for damn in dummy:
            corpus+= '\n'
            print(damn)
            corpus+= str(dummy[damn])
        #TODO
    
    texto.delete(1.0,END)
    texto.insert(INSERT,corpus)
    

def agregar_obra(data):
    trial = data[2].get()
    trial1 = trial.replace(' ','')
    if trial1 == '' or trial in data[0]['values']:
        messagebox.showerror('Error al Agregar', 'La obra ya existe o el nombre no es válido.')
    else: 
        lul = []
        global def_values
        for i in def_values:
            lul.append(i)
        lul.append(data[2].get())
        lul = tuple(lul)
        data[0]['values'] = lul
        def_values = lul
        actualizar_valores(data,'')

def registrar_transaccion():
    pass

def ver_reporte():
    pass



__main__()