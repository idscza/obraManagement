# -*- coding: utf-8 -*-
"""
@author: Ditto Castform
"""

from tkinter import *
import mockup as mu

def __main__():
    window = Tk()
    window.title("Manejo de Presupuesto")
    menus = Menu(window)
    menus = Menu(window)
 
    new_item = Menu(menus)
 
    new_item.add_command(label='Cargar Obras')
    new_item.add_command(label='Seleccionar Obra')
 
    menus.add_cascade(label='Obras', menu=new_item)
    window.config(menu=menus)

    lbl = Label(window, text="Hello",font=("Times New Roman",50))
    lbl.grid(column=0, row=1)
    window.geometry('1050x550')
    btn = Button(window, text="Click Me")
    btn.grid(column=0, row=2)
    window.mainloop()




__main__()