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

class main:
    def __init__(self,window):
        self.window = window
        self.window.title("Manejo de Presupuesto")
        self.window.geometry('945x270')
    
        global def_values
        mu.generate_mockups(def_values)

        self.lbl = Label(window, text="Bienvenidos al Manejador \nde Presupuestos de Obras",font=("Arial",20))
        self.lbl.grid(column=0, row=1)

        self.lbl1 = Label(window, text=' ')
        self.lbl1.grid(column=1,row=0)
    
        self.lbl2 = Label(window, text='         ')
        self.lbl2.grid(column=1,row=1)
    
        self.txt = scrolledtext.ScrolledText(window,width=70,height=10)
        self.txt.grid(column=2, row=1)
        
        self.monto = Entry(window,width=25,state='disabled')
        self.monto.grid(column=2, row=2, sticky = (E))
    
        self.combochoice = Combobox(window,width=25)
        self.combochoice.grid(column=2, row=2)
    
        self.nomrub = Entry(window,width=28,state='disabled')
        self.nomrub.grid(column=2, row=3)
    
        self.cant = Entry(window,width=25,state='disabled')
        self.cant.grid(column=2, row=3, sticky = (E))
    
    
        self.btnx = Button(window,text="try",command= lambda: self.open_t(ventana_agregar_rubro))
        self.btnx.grid(column=3,row=1)
    
        self.combo = Combobox(window,width=32)
        self.forz_act = partial(actualizar_valores,[self.combo,self.txt,self.combochoice])
        self.window.bind('<<ComboboxSelected>>', self.forz_act)

        self.combo.grid(column = 0, row = 3, sticky = (E))
    
        self.lbl2 = Label(window, text='       Obras\n     Actuales')
        self.lbl2.grid(column = 0, row = 3, sticky = (W))
    
    
        self.nomobra = Entry(window,width=35,state='disabled')
        self.nomobra.grid(column=0, row=2, sticky = (E))
    
        self.agob=partial(agregar_obra,[self.combo,self.txt,self.combochoice,self.nomobra])
        self.btn = Button(window, text="Agregar\n  Obra",command=self.agob,state='disabled')
        self.btn.grid(column=0, row=2, sticky = (W))
    
    
        self.regtran=partial(registrar_transaccion,[self.combo,self.txt,self.combochoice,self.monto])
        self.btn1 = Button(window, text="Registrar Transacción",command=self.regtran,state='disabled')
        self.btn1.grid(column=2, row=2, sticky = (W))
    
    
        self.agg_rub=partial(agregar_rubro,[self.combo,self.txt,self.combochoice,self.nomrub,self.cant])
        self.btn2 = Button(window, text="Agregar Rubro            ",command=self.agg_rub,state='disabled')
        self.btn2.grid(column=2, row=3, sticky = (W))
    
        self.menus = Menu(window)
 
        self.new_item = Menu(self.menus)

        self.cheat = partial(cargar_obras,[self.combo,self.txt,self.combochoice,
                                           self.monto,self.btn,self.nomobra,self.btn1,
                                           self.btn2,self.nomrub,self.cant])   
    #new_item.add_command(label='Cargar Obras',command=cheat)
        self.new_item.add_command(label='Cargar Obras',command=lambda: self.open_t(ventana_iniciar_sesion))
    #new_item.add_command(label='Seleccionar Obra')
    
        self.menus.add_cascade(label='Obras', menu=self.new_item)
        self.window.config(menu=self.menus) 
        self.window.resizable(False, False)

    
    def activar_todo():
        print("Cáceres se la come")
            
    def open_t(self,_class):	
        self.temp = Toplevel(self.window)
        _class(self.temp,self.window,mu)


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

def agregar_rubro1(data):
    rta = mu.agregar_rubro(data[0],data[3],data[4])
    if rta[0] == False:
        messagebox.showerror('Error al Crear Rubro', rta[1])
    else:
        messagebox.showerror('cOPASo', rta[1])


class login:
	def __init__(self, master):
		self.master = master
		self.master.geometry("400x400+200+200")
		self.frame = Frame(self.master)
		self.quit = Button(self.frame, text = f"Quit this window n. ", command = self.close_window)
		self.quit.pack()
		self.frame.pack()
 
	def close_window(self):
		self.master.destroy()
        
class ventana_agregar_rubro:
    def __init__(self, master, parent, mu):
        mu = mu
        self.master = master
        self.master.geometry("250x150")
        self.frame = Frame(self.master)
        self.quit = Button(self.frame, text = " Salir ", command = self.close_window)
        self.lbl1 = Label(self.frame,text="Ingrese Nombre del Rubro",font=("Arial",10))
        self.entr1 = Entry(self.frame,width=35)
        self.lbl2 = Label(self.frame,text="Ingrese Presupuesto",font=("Arial",10))
        self.entr2 = Entry(self.frame,width=35)
        self.agregar = Button(self.frame, text = "Agregar", command = lambda: agregar_rubro1(["Los Alpes",0,0,"Putas","1000"]))
        self.lbl1.pack()
        self.entr1.pack()
        self.lbl2.pack()
        self.entr2.pack()
        self.quit.pack()
        self.agregar.pack()
        self.master.resizable(False, False)
        self.frame.pack()
 
    def close_window(self):
        self.master.destroy()

class ventana_agregar_transaccion:
    def __init__(self, master, parent, mu):
        mu = mu
        self.master = master
        self.master.geometry("250x150")
        self.frame = Frame(self.master)
        self.quit = Button(self.frame, text = " Salir ", command = self.close_window)
        self.lbl1 = Label(self.frame,text="Seleccionar Nombre del Rubro",font=("Arial",10))
        self.cbb = Combobox(self.frame,width=32)
        self.lbl2 = Label(self.frame,text="Ingrese Nuevo Egreso",font=("Arial",10))
        self.entr2 = Entry(self.frame,width=35)
        self.agregar = Button(self.frame, text = "Agregar", command = lambda: agregar_rubro1(["Los Alpes",0,0,"Putas","1000"]))
        self.lbl1.pack()
        self.cbb.pack()
        self.lbl2.pack()
        self.entr2.pack()
        self.quit.pack()
        self.agregar.pack()
        self.master.resizable(False, False)
        self.frame.pack()
 
    def close_window(self):
        self.master.destroy()
        
class ventana_iniciar_sesion:
    def __init__(self, master, parent, mu):
        print(type(parent))
        self.mu = mu
        self.master = master
        self.parent = parent
        self.master.geometry("250x150")
        self.frame = Frame(self.master)
        self.quit = Button(self.frame, text = " Cancelar ", command = self.close_window)
        self.lbl1 = Label(self.frame,text="Usuario",font=("Arial",10))
        self.entr1 = Entry(self.frame,width=35)
        self.lbl2 = Label(self.frame,text="Contraseña",font=("Arial",10))
        self.entr2 = Entry(self.frame,show="*",width=35)
        self.agregar = Button(self.frame, text = "Agregar", command = lambda: self.iniciar_sesion(self.mu,self.entr1,self.entr2))
        self.lbl1.pack()
        self.entr1.pack()
        self.lbl2.pack()
        self.entr2.pack()
        self.quit.pack()
        self.agregar.pack()
        self.master.resizable(False, False)
        self.frame.pack()
 
    def close_window(self):
        self.master.destroy()

    def iniciar_sesion(self,mu,usr,pw):
        trial = mu.pwcombo
        theusr = usr.get().lower()
        if theusr not in trial.keys():
            messagebox.showerror('Error', 'Usuario no encontrado')
        elif trial[theusr] != pw.get():
            messagebox.showerror('Error', 'Contraseña inválida')
        else:
            main.activar_todo()
            pass
        self.master.destroy()

root = Tk()
app = main(root)
root.mainloop()
