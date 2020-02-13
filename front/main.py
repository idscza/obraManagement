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
    window.geometry('945x270')

    global def_values
    mu.generate_mockups(def_values)

    lbl = Label(window, text="Bienvenidos al Manejador \nde Presupuestos de Obras",font=("Arial",20))
    lbl.grid(column=0, row=1)

    lbl1 = Label(window, text=' ')
    lbl1.grid(column=1,row=0)
    
    lbl2 = Label(window, text='         ')
    lbl2.grid(column=1,row=1)
    
    txt = scrolledtext.ScrolledText(window,width=70,height=10)
    txt.grid(column=2, row=1)
    
 
    
    monto = Entry(window,width=25,state='disabled')
    monto.grid(column=2, row=2, sticky = (E))
    
    combochoice = Combobox(window,width=25)
    combochoice.grid(column=2, row=2)
    
    
    btn2 = Button(window, text="Agregar Rubro            ",state='disabled')
    btn2.grid(column=2, row=3, sticky = (W))
    
    nomrub = Entry(window,width=28,state='disabled')
    nomrub.grid(column=2, row=3)
    
    cant = Entry(window,width=25,state='disabled')
    cant.grid(column=2, row=3, sticky = (E))
    
    
    '''btn3 = Button(window, text="Ver Reporte",state='disabled')
    btn3.grid(column=2, row=3, sticky = (W))'''
     
    combo = Combobox(window,width=32)
    forz_act = partial(actualizar_valores,[combo,txt,combochoice])
    window.bind('<<ComboboxSelected>>', forz_act)

    combo.grid(column = 0, row = 3, sticky = (E))
    
    lbl2 = Label(window, text='       Obras\n     Actuales')
    lbl2.grid(column = 0, row = 3, sticky = (W))
    
    
    nomobra = Entry(window,width=35,state='disabled')
    nomobra.grid(column=0, row=2, sticky = (E))
    
    agob=partial(agregar_obra,[combo,txt,combochoice,nomobra])
    btn = Button(window, text="Agregar\n  Obra",command=agob,state='disabled')
    btn.grid(column=0, row=2, sticky = (W))
    
    
    regtran=partial(registrar_transaccion,[combo,txt,combochoice,monto])
    btn1 = Button(window, text="Registrar Transacción",command=regtran,state='disabled')
    btn1.grid(column=2, row=2, sticky = (W))
    
    
    agg_rub=partial(agregar_rubro,[combo,txt,combochoice,nomrub,cant])
    btn2 = Button(window, text="Agregar Rubro            ",command=agg_rub,state='disabled')
    btn2.grid(column=2, row=3, sticky = (W))
    
    menus = Menu(window)
 
    new_item = Menu(menus)

    cheat = partial(cargar_obras,[combo,txt,combochoice,monto,btn,nomobra,btn1,btn2,nomrub,cant])   
    new_item.add_command(label='Cargar Obras',command=cheat)
    #new_item.add_command(label='Seleccionar Obra')
    
    menus.add_cascade(label='Obras', menu=new_item)
    
    
    
    window.config(menu=menus) 
    window.resizable(False, False)
    window.mainloop()

#Totally Mockup, it should call SQL DB
def cargar_obras(data):
    global def_values
    data[0]['values'] = def_values
    data[0].current(0)
    data[6].state(['!disabled'])
    data[7].state(['!disabled'])
    data[8].state(['!disabled'])
    data[9].state(['!disabled'])
    data[4].state(['!disabled'])
    data[5].state(['!disabled'])
    data[3].state(['!disabled'])
    actualizar_valores(data,'')

def actualizar_valores(data,x):
    name = data[0].get()
    texto = data[1]
    corpus = ''
    
    corpus = name
    mud = mu.get_mockup(name)
    
    global actual
    actual = mud
    
    mud1 = {'Entradas':mud['Entradas'],
            'Salidas':mud['Salidas']}
    
    vals = []
    
    for val in mud1:
        corpus+= '\n\n'
        dummy = mud1[val]
        corpus+=val
        corpus+=":"
        for damn in dummy:
            corpus+= '\n'
            corpus+= damn
            corpus+=':  \t'
            if type(dummy[damn]) == int:
                corpus+= str(dummy[damn])
            else:
                corpus+='P: '
                corpus+= str(dummy[damn][0])
                corpus+='\tG: '
                corpus+= str(dummy[damn][1])
            vals.append(damn)
   
    vals1 = tuple(vals)
    data[2]['values']=vals1
    #data[2].current(0)
    
    texto.delete(1.0,END)
    texto.insert(INSERT,corpus)
    

def agregar_obra(data):
    trial = data[3].get()
    trial1 = trial.replace(' ','')
    if trial1 == '' or trial in data[0]['values']:
        messagebox.showerror('Error al Agregar', 'La obra ya existe o el nombre no es válido.')
    else: 
        lul = []
        global def_values
        for i in def_values:
            lul.append(i)
        lul.append(data[3].get())
        lul = tuple(lul)
        data[0]['values'] = lul
        def_values = lul
        actualizar_valores(data,'')

def registrar_transaccion(data):
    rta = mu.registrar_transaccion(data[0].get(),data[2].get(),data[3].get())
    if rta[0] == False:
        messagebox.showerror('Error al Registrar', rta[1])
    else:
        actualizar_valores(data,'')


def agregar_rubro(data):
    rta = mu.agregar_rubro(data[0].get(),data[3].get(),data[4].get())
    if rta[0] == False:
        messagebox.showerror('Error al Crear Rubro', rta[1])
    else:
        actualizar_valores(data,'')


__main__()