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
import sqlAccess as sql
from functools import partial
import datetime


class main:
    def __init__(self,window):
        self.window = window
        self.window.title("Manejo de Presupuesto")
        self.window.geometry('960x270')
        
        self.actual_user = StringVar()
        self.actual_obra = IntVar()

        self.lbl = Label(window, text="  Bienvenidos al Manejador \n de Presupuestos de Obras",font=("Arial",20))
        self.lbl.grid(column=0, row=1)

        self.lbl1 = Label(window, text=' ')
        self.lbl1.grid(column=1,row=0)
    
        self.lbl2 = Label(window, text='         ')
        self.lbl2.grid(column=1,row=1)
    
        self.txt = scrolledtext.ScrolledText(window,width=70,height=10)
        self.txt.grid(column=2, row=1)
    
        self.combo = Combobox(window,width=32)
        self.window.bind('<<ComboboxSelected>>', self.actualizar_valoress)

        self.combo.grid(column = 0, row = 2, sticky = (E))
    
        self.lbl2 = Label(window, text='       Obras\n     Actuales')
        self.lbl2.grid(column = 0, row = 2, sticky = (W))
    
        self.btn = Button(window, text="Agregar\n  Obra",state='disabled'
                          ,command= lambda: self.ventana_agregar_o(Toplevel(self.window)))
        self.btn.grid(column=0, row=3)
    
        self.btn1 = Button(window, text="Agregar Rubro            ",
                           command = lambda: self.ventana_agregar_r(Toplevel(self.window)),
                           state='disabled')
        self.btn1.grid(column=2, row=2, sticky = (W))
    
        self.btn2 = Button(window, text="Registrar Transacción",
                           command=lambda: self.ventana_agregar_t(Toplevel(self.window))
                               ,state='disabled')
        self.btn2.grid(column=2, row=2)
        
        self.menus = Menu(window)
 
        self.new_item = Menu(self.menus)
        
        self.menus.add_command(label='Iniciar Sesión',
                    command=lambda: self.ventana_iniciar(Toplevel(self.window)))
        self.menus.add_command(label='Crear Usuario',state='disabled',
                    command=lambda: self.ventana_nuevo_usuario(Toplevel(self.window)))
        self.menus.add_command(label='Cerrar Sesión',state='disabled',
                               command = self.cerrar_sesion)

        self.window.config(menu=self.menus) 

        self.window.resizable(False, False)
        
    def activar_todo(self):          
        messagebox.showinfo('Bienvenido','Sesión iniciada con éxito')
        self.menus.entryconfig('Iniciar Sesión',state='disabled')
        self.menus.entryconfig("Crear Usuario",state='normal')
        self.menus.entryconfig("Cerrar Sesión",state='normal')
        self.cargar_obras()
        self.actualizar_valores()
    
    def cargar_obras(self):
        vals = sql.select_all_obras()
        self.combo['values'] = vals
        try:
            self.combo.current(0)
        except:
            pass
        self.btn2.state(['!disabled'])
        self.btn1.state(['!disabled'])
        self.btn.state(['!disabled'])
       
        
    def actualizar_valoress(self,machete):
        self.actualizar_valores()
    
    def actualizar_valores(self):
        name = self.combo.get()
        self.actual_obra = name.split(".")[0].replace('.','')
        texto = self.txt
        corpus = ''
      
        corpus = name
        
        trans = sql.select_transacciones_obra(self.actual_obra)
        print(trans)
        print(self.actual_obra)
        
        synth = self.analizar_transacciones(trans)
    
        for val in synth:
            corpus+= '\n----------------------------------------------------------------------'
            corpus+= '\t\t\t\t    '+val
            corpus+= '\n----------------------------------------------------------------------'
            dummy = synth[val]
            for damn in dummy:
                corpus+= '\n'
                corpus+= damn
                corpus+=':  \t'
                if type(dummy[damn]) != list:
                    corpus+= str(dummy[damn])
                else:
                    corpus+='P: '
                    corpus+= str(dummy[damn][0])
                    corpus+='\tG: '
                    corpus+= str(dummy[damn][1])               

        texto.delete(1.0,END)
        texto.insert(INSERT,corpus)
    
    def analizar_transacciones(self,lista):
        xd = {"INGRESOS":{},
              "EGRESOS":{}}
        for i in lista:
            if i[5] == "Entrada":
                if xd['INGRESOS'].get(i[3]) is None:
                    xd['INGRESOS'][i[3]] = i[4]
                else:
                    xd['INGRESOS'][i[3]] += i[4]
            elif i[5] == "Presupuesto":
                xd['EGRESOS'][i[3]] = [i[4],0]
            else:
                if xd['EGRESOS'].get(i[3]) is None:
                    xd['EGRESOS'][i[3]] = [0,i[4]]
                else:
                    xd['EGRESOS'][i[3]][1] += i[4]
        return xd
            
    def agregar_obr(self,nm,ct,dr,ie,fim,fid,fia,fcm,fcd,fca):
        yd = {'ENE':1,'FEB':2,'MAR':3,'ABR':4,'MAY':5,'JUN':6,
             'JUL':7,'AGO':8,'SEP':9,'OCT':10,'NOV':11,'DIC':12}
        ini = main.validar_fecha(yd[fim],int(fid),int(fia))
        cul = main.validar_fecha(yd[fcm],int(fcd),int(fca))
        fat = False
        if int(fca) < int(fia):
            fat = True
        elif int(fca) == int(fia) and yd[fcm] < yd[fim]:
            fat = True
        elif int(fca) == int(fia) and yd[fcm] == yd[fim] and int(fcd) <= int(fid):
            fat = True
        if not(ini and cul):
            messagebox.showerror('Error', 'Las Fechas no son Válidas')
            return
        elif fat:
            messagebox.showerror('Error', 'La Obra no puede empezar después de terminar')
            return
        if nm.strip() == '' or ct.strip() == '' or dr.strip() == '' or ie.strip() == '':
            messagebox.showerror('Error', 'La obra no puede registrarse con campos vacíos')
            return
        fi = str(fid) + '-' + str(yd[fim]) + "-" + str(fia)
        fc = str(fcd) + '-' + str(yd[fcm]) + "-" + str(fca)
        try:
            helper = sql.create_obra((nm,ct,dr,ie,fi,fc))
            messagebox.showinfo('Crear Obra','Obra creada con éxito')
            sql.create_transaccion((helper,self.actual_user,"Inversionistas",0,"Entrada",0))
            sql.create_transaccion((helper,self.actual_user,"Ventas",0,"Entrada",0))
            sql.create_transaccion((helper,self.actual_user,"Préstamos",0,"Entrada",0))
            #TODO Diversificar rubros de entrada
        except:
            messagebox.showerror('Error','La obra no pudo ser creada')
        self.cargar_obras()
        self.actualizar_valores()
        
    def validar_fecha(m,d,a):
        isValidDate = True
        try :
            datetime.datetime(a,m,d)
        except ValueError :
            isValidDate = False
        return isValidDate
    
    def agregar_rub(self,nombre,valor,presupuestado):
        
        hue = sql.select_transacciones_obra(self.actual_obra)
        
        for fact in hue:
            if nombre == fact[3]:
                messagebox.showerror('Error','El rubro ya existe')
                return
        if presupuestado:
            sql.create_transaccion((self.actual_obra,
                                    self.actual_user,
                                    nombre,
                                    valor,
                                    'Presupuesto',
                                    1))
            messagebox.showinfo('Crear Rubro','Rubro creado con éxito')
            self.actualizar_valores()
        else:
            sepuede = self.verificar_dinero(hue,valor)
            if sepuede:
                sql.create_transaccion((self.actual_obra,
                                    self.actual_user,
                                    nombre,
                                    valor,
                                    'Gasto',
                                    0))            
                messagebox.showinfo('Crear Rubro','Rubro creado con éxito')
                self.actualizar_valores()
            else:
                messagebox.showerror('Error','El rubro excede el dinero disponible')
    
    def agregar_transac(self,nombre,valor):
        
        hue = sql.select_transacciones_obra(self.actual_obra)
        
        verify = nombre.split(": ")[0]
        realname = nombre.split(": ")[1]
        
        if verify == "Entrada":
            sql.create_transaccion((self.actual_obra,
                                    self.actual_user,
                                    realname,
                                    valor,
                                    'Entrada',
                                    1))
            messagebox.showinfo('Crear Rubro','Rubro creado con éxito')
            self.actualizar_valores()
        else:
            sepuede = self.verificar_dinero(hue,valor)
            if sepuede:
                sql.create_transaccion((self.actual_obra,
                                    self.actual_user,
                                    realname,
                                    valor,
                                    'Gasto',
                                    0))            
                messagebox.showinfo('Registrar Transacción','Factura creada con éxito')
                self.actualizar_valores()
            else:
                messagebox.showerror('Error','El rubro excede el dinero disponible')
                
    def verificar_dinero(self,facturas, valor):
        suma = 0
        gasto = 0
        for factura in facturas:
            if factura[5] == 'Gasto':
                gasto+=factura[4]
            elif factura[5] == 'Entrada':
                suma+=factura[4]
        if suma > gasto+valor:
            return True
        else:
            return False
        
    #Ventana para iniciar Sesión
    
    def ventana_iniciar(self, master):
        self.master = master
        self.master.geometry("250x150")
        self.frame = Frame(self.master)
        
        def close_window(self):
            self.master.destroy()

        def iniciar_sesion(usr,pw):
            trial = sql.select_all_users()
            theusr = usr.get().lower()
            if theusr not in trial.keys():
                messagebox.showerror('Error', 'Usuario no encontrado')
            elif trial[theusr] != pw.get():
                messagebox.showerror('Error', 'Contraseña inválida')
            else:
                self.actual_user = theusr
                main.activar_todo(self) 
            self.master.destroy()

        self.quit = Button(self.frame, text = " Cancelar ", 
                           command = lambda : close_window(self))
        self.lblus = Label(self.frame,text="Usuario",font=("Arial",10))
        self.entrus = Entry(self.frame,width=35)
        self.lblpw = Label(self.frame,text="Contraseña",font=("Arial",10))
        self.entrpw = Entry(self.frame,show="*",width=35)
        self.blank = Label(self.frame,text=" ")
        self.agregar = Button(self.frame, text = "Iniciar Sesión", 
                              command = lambda: iniciar_sesion(self.entrus,self.entrpw))
        self.lblus.pack()
        self.entrus.pack()
        self.lblpw.pack()
        self.entrpw.pack()
        self.blank.pack()
        self.quit.pack(side = "left")
        self.agregar.pack(side = "right")
        self.master.resizable(False, False)
        self.frame.pack()
    
    #Ventana para Agregar Usuario
    def ventana_nuevo_usuario(self,master):
        self.master = master
        self.master.geometry("250x230")
        self.frame = Frame(self.master)
         
        def close_window(self):
            self.master.destroy()
        
        def agregar_el_user(usr,pw,pw2,nm):
            trial = sql.select_all_users()
            theusr = usr.get().lower()
            if theusr in trial.keys():
                messagebox.showerror('Error', 'El usuario ya existe')
            elif pw2.get()!= pw.get():
                messagebox.showerror('Error', 'Las contraseñas deben coincidir')
            elif pw.get() == '':
                messagebox.showerror('Error', 'Las contraseña no debe ser vacía')
            else:
                sql.create_user((theusr,pw.get(),nm.get()))
                messagebox.showinfo('Éxito','Se ha agregado el usuario')
            self.master.destroy()
        self.quit = Button(self.frame, text = " Cancelar ", 
                           command = lambda : close_window(self))
        self.lblus = Label(self.frame,text="Nuevo Usuario",font=("Arial",10))
        self.entrus = Entry(self.frame,width=35)
        self.lblnm = Label(self.frame,text="Nombre",font=("Arial",10))
        self.entrnm = Entry(self.frame,width=35)
        self.lblpw = Label(self.frame,text="Contraseña",font=("Arial",10))
        self.entrpw = Entry(self.frame,show="*",width=35)
        self.lblpw2 = Label(self.frame,text="Confirme la contraseña",font=("Arial",10))
        self.entrpw2 = Entry(self.frame,show="*",width=35)
        self.blank = Label(self.frame,text=" ")
        self.agregar = Button(self.frame, text = "Registrar", 
                              command = lambda: agregar_el_user(self.entrus,
                                                                self.entrpw,
                                                                self.entrpw2,
                                                                self.entrnm))
        self.lblus.pack()
        self.entrus.pack()
        self.lblnm.pack()
        self.entrnm.pack()
        self.lblpw.pack()
        self.entrpw.pack()
        self.lblpw2.pack()
        self.entrpw2.pack()
        self.blank.pack()
        self.quit.pack(side = "left")
        self.agregar.pack(side = "right")
        self.master.resizable(False, False)
        self.frame.pack()
    
    #Ventana para Cerrar Sesión
    def cerrar_sesion(self):
        choice = messagebox.askyesno(title="Cerrar Sesión", message="¿Desea Cerrar Sesión?")
        if choice:
            self.menus.entryconfig('Iniciar Sesión',state='normal')
            self.menus.entryconfig("Crear Usuario",state='disabled')
            self.menus.entryconfig("Cerrar Sesión",state='disabled')
            self.actual_user = ''
            self.actual_obra = 0
            self.txt.delete(1.0,END)
            self.combo['values'] = ()
            self.combo.delete(0,END)
            self.btn2.state(['disabled'])
            self.btn1.state(['disabled'])
            self.btn.state(['disabled'])
            #self.monto.state(['disabled'])
            
    #Ventana para Agregar Obra
    
    def ventana_agregar_o(self,master):
        self.master = master
        self.master.geometry("250x300")
        self.frame = Frame(self.master)
          
        def close_window(self):
            self.master.destroy()
        
        def agregar_la_obra(self,nm,ct,dr,ie,fim,fid,fia,fcm,fcd,fca):
            main.agregar_obr(self,nm.get(),
                             ct.get(),
                             dr.get(),
                             ie.get(),
                             fim.get(),
                             fid.get(),
                             fia.get(),
                             fcm.get(),
                             fcd.get(),
                             fca.get())
            self.master.destroy()
            
        self.quit = Button(self.frame, text = " Salir ",
                           command = lambda : close_window(self))
        self.lbla = Label(self.frame,text="Nombre de la Obra",font=("Arial",10))
        self.entra = Entry(self.frame,width=35)
        self.lblb = Label(self.frame,text="Ciudad",font=("Arial",10))
        self.entrb = Entry(self.frame,width=35)
        self.lblc = Label(self.frame,text="Dirección",font=("Arial",10))
        self.entrc = Entry(self.frame,width=35)
        self.lbld = Label(self.frame,text="Ingeniero Encargado",font=("Arial",10))
        self.entrd = Entry(self.frame,width=35)
        self.lble = Label(self.frame,text="Fecha Inicio",font=("Arial",10))
        self.combe1 = Combobox(self.frame,width=8)        
        self.combe1['values'] = ('ENE','FEB','MAR','ABR','MAY','JUN',
                                 'JUL','AGO','SEP','OCT','NOV','DIC')
        self.combe1.current(0)
        self.combe2 = Combobox(self.frame,width=8)
        self.combe2['values'] = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
                                 16,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
        self.combe2.current(0)
        self.combe3 = Combobox(self.frame,width=8)
        self.combe3['values'] = (2015,2016,2017,2018,2019,2020,2021,2022,2023,
                                  2024,2025,2026,2027,2028,2029,2030,2031,2032,
                                  2033,2034,2035)
        self.combe3.current(0)
        self.lblf = Label(self.frame,text="Fecha Culminación",font=("Arial",10))
        self.combf1 = Combobox(self.frame,width=8)        
        self.combf1['values'] = ('ENE','FEB','MAR','ABR','MAY','JUN',
                                 'JUL','AGO','SEP','OCT','NOV','DIC')
        self.combf1.current(0)
        self.combf2 = Combobox(self.frame,width=8)
        self.combf2['values'] = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
                                 16,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
        self.combf2.current(0)
        self.combf3 = Combobox(self.frame,width=8)
        self.combf3['values'] = (2015,2016,2017,2018,2019,2020,2021,2022,2023,
                                  2024,2025,2026,2027,2028,2029,2030,2031,2032,
                                  2033,2034,2035)
        self.combf3.current(0)
        self.agregar = Button(self.frame, text = "Agregar",
                              command = lambda: agregar_la_obra(self,
                                                                self.entra,
                                                                self.entrb,
                                                                self.entrc,
                                                                self.entrd,
                                                                self.combe1,
                                                                self.combe2,
                                                                self.combe3,
                                                                self.combf1,
                                                                self.combf2,
                                                                self.combf3)) 
        self.blank = Label(self.frame,text=" ")
        self.lbla.grid(column=0,row=0)
        self.entra.grid(column=0,row=1)
        self.lblb.grid(column=0,row=2)
        self.entrb.grid(column=0,row=3)
        self.lblc.grid(column=0,row=4)
        self.entrc.grid(column=0,row=5)
        self.lbld.grid(column=0,row=6)
        self.entrd.grid(column=0,row=7)
        self.lble.grid(column=0,row=8)
        self.combe1.grid(column=0,row=9, sticky = (W))
        self.combe2.grid(column=0,row=9)
        self.combe3.grid(column=0,row=9, sticky = (E))
        self.lblf.grid(column=0,row=10)
        self.combf1.grid(column=0,row=11, sticky = (W))
        self.combf2.grid(column=0,row=11)
        self.combf3.grid(column=0,row=11, sticky = (E))
        self.blank.grid(column=0,row=12)
        self.quit.grid(column=0,row=13, sticky = (W))
        self.agregar.grid(column=0,row=13, sticky = (E))
        self.master.resizable(False, False)
        self.frame.pack()        
    
    #Ventana para Agregar Rubro
    
    def ventana_agregar_r(self,master):
        self.master = master
        self.master.geometry("250x150")
        self.frame = Frame(self.master)
        self.huh = IntVar()
          
        def close_window(self):
            self.master.destroy()      
        
        def agregar_el_rubro(self,nombre,valor,presu):
            try:
                float(valor.get())
                main.agregar_rub(self,
                                 nombre.get(),
                                 float(valor.get()),
                                 presu.get())
                self.master.destroy()
            except:
                messagebox.showerror('Error', 'Ingrese un valor númerico para el valor del rubro')      
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        self.lblm = Label(self.frame,text="Ingrese Nombre del Rubro",font=("Arial",10))
        self.entrm = Entry(self.frame,width=35)
        self.lbln = Label(self.frame,text="Ingrese Presupuesto",font=("Arial",10))
        self.entrn = Entry(self.frame,width=35)
        self.checkbox = Checkbutton(self.frame, text="¿El rubro fue presupuestado?",
                                    variable=self.huh)
        self.agregar = Button(self.frame, text = "Agregar",
                              command = lambda: agregar_el_rubro(self,
                                                                 self.entrm,
                                                                 self.entrn,
                                                                 self.huh))
        self.lblm.pack()
        self.entrm.pack()
        self.lbln.pack()
        self.entrn.pack()
        self.checkbox.pack()
        self.quit.pack(side = "left")
        self.agregar.pack(side = "right")
        self.master.resizable(False, False)
        self.frame.pack()

    
    #Ventana para Agregar Transacción
    def ventana_agregar_t(self,master):
        self.master = master
        self.master.geometry("250x150")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()      
        
        def agregar_trans(self,nombre,valor):
            try:
                float(valor.get())
                main.agregar_transac(self,
                                 nombre.get(),
                                 float(valor.get()))
                self.master.destroy()
            except:
                messagebox.showerror('Error', 'Ingrese un valor númerico para el valor del rubro') 
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        self.lbly = Label(self.frame,text="Seleccionar Rubro",font=("Arial",10))
        
        self.cbb = Combobox(self.frame,width=32)
        self.cbb['values'] = sql.get_rubros_obra(self.actual_obra)
        self.cbb.current(0)
        self.lblu = Label(self.frame,text="Ingrese Nueva Factura",font=("Arial",10))
        self.entru = Entry(self.frame,width=35)
        self.agregar = Button(self.frame, text = "Agregar", 
                              command = lambda: agregar_trans(self,
                                                              self.cbb,
                                                              self.entru))
        self.blank = Label(self.frame,text=" ")
        self.lbly.pack()
        self.cbb.pack()
        self.lblu.pack()
        self.entru.pack()
        self.blank.pack()
        self.quit.pack(side = "left")
        self.agregar.pack(side = "right")
        self.master.resizable(False, False)
        self.frame.pack()
  
        
    #Ventana para ver Historial Facturas
    
    #Ventana para ver graficas de obra


#Totally Mockup, it should call SQL DB


def registrar_transaccion(data):
    rta = mu.registrar_transaccion(data[0].get(),data[2].get(),data[3].get())
    if rta[0] == False:
        messagebox.showerror('Error al Registrar', rta[1])
    else:
        #actualizar_valores(data,'')
        pass


 
    def close_window(self):
        self.master.destroy()       

root = Tk()
app = main(root)
root.mainloop()
