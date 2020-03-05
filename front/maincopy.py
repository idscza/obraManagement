# -*- coding: utf-8 -*-
"""

Esqueleto de programa de manejo de presupuesto de obras

@author: Ditto Castform
"""

from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import *
import sqlAccess as sql
import datetime
from PIL import Image, ImageTk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np


class main:
    def __init__(self,window):
        
        self.master = None
        self.window = window
        self.window.title("Manejo de Obras")
        self.window.geometry('960x660')
        
        self.actual_user = StringVar()
        self.actual_obra = IntVar()

        self.lbljaja = Label(window, text="",font=("Arial",12))
        self.lbljaja.grid(column=0, row=1, sticky =(N))
        
        self.lbljiji = Label(window, text="",font=("Arial",12))
        self.lbljiji.grid(column=0, row=1, sticky =(S))
       
        '''fig = Figure(figsize=(3, 1), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        self.labeljiji = FigureCanvasTkAgg(fig, master=self.window)  # A tk.DrawingArea.
        self.labeljiji.draw()
        self.labeljiji.grid(column=0, row=1, sticky =(S))'''

        
        self.photo = Image.open("pic.png")
        self.thephoto = ImageTk.PhotoImage(self.photo)
        self.lbl = Label(window,image=self.thephoto)
        self.lbl.grid(column=0, row=1)
        self.lbl.image = self.thephoto

        self.lbl1 = Label(window, text=' ')
        self.lbl1.grid(column=1,row=0)
    
        self.lbl2 = Label(window, text='         ')
        self.lbl2.grid(column=1,row=1)
    
        self.txt = scrolledtext.ScrolledText(window,width=70,height=35)
        self.txt.grid(column=2, row=1)
    
        self.combo = Combobox(window,width=32)
        self.window.bind('<<ComboboxSelected>>', self.actualizar_valoress)

        self.combo.grid(column = 0, row = 2, sticky = (E))
    
        self.lbl2 = Label(window, text='       Obras\n     Actuales')
        self.lbl2.grid(column = 0, row = 2, sticky = (W))
    
        self.btn = Button(window, text="Agregar\n  Obra",state='disabled'
                          ,command= lambda: self.ventana_agregar_o(Toplevel(self.window)))
        self.btn.grid(column=0, row=3, sticky = (W))
        
        self.btn7 = Button(window, text="Editar\nObra",state='disabled'
                          ,command= lambda: self.ventana_editar_o(Toplevel(self.window)))
        self.btn7.grid(column=0, row=3, sticky = (E))
        
        self.btn8 = Button(window, text="      Editar\nPresupuesto",state='disabled'
                          ,command= lambda: self.ventana_editar_p(Toplevel(self.window)))
        self.btn8.grid(column=0, row=3)
    
        self.btn1 = Button(window, text="Agregar Rubro            ",
                           command = lambda: self.ventana_agregar_r(Toplevel(self.window)),
                           state='disabled')
        self.btn1.grid(column=2, row=2, sticky = (W))
        
        
        self.btn3 = Button(window, text="Mostrar Facturas         ",
                           command = lambda: self.ventana_mostrar_f(Toplevel(self.window)),
                           state='disabled')
        self.btn3.grid(column=2, row=2, sticky = (E))
    
        self.btn2 = Button(window, text="Registrar Transacción",
                           command=lambda: self.ventana_agregar_t(Toplevel(self.window))
                               ,state='disabled')
        self.btn2.grid(column=2, row=2)
        
        self.btn4 = Button(window, text="        Ver Clientes         ",
                           command=lambda: self.ventana_agregar_t(Toplevel(self.window))
                               ,state='disabled')
        #self.btn4.grid(column=2, row=3)
        
        self.btn5 = Button(window, text="Información Obra       ",
                           command=lambda: self.ventana_info_obra(Toplevel(self.window))
                               ,state='disabled')
        self.btn5.grid(column=2, row=3, sticky = (E))
        
        self.btn6 = Button(window, text="Ver Gráficas                 ",
                           command=lambda: self.ver_graficas(Toplevel(self.window))
                               ,state='disabled')
        self.btn6.grid(column=2, row=3, sticky = (W))
        
        self.menus = Menu(window)
 
        
        self.menus.add_command(label='Iniciar Sesión',
                    command=lambda: self.ventana_iniciar(Toplevel(self.window)))
        self.menus.add_command(label='Estado General',state='disabled',
                    command=lambda: self.ventana_estadogeneral(Toplevel(self.window)))     
        self.cascada = Menu(self.menus,tearoff=0)
        self.cascada.add_command(label='Ver Clientes',
                    command=lambda: self.ventana_mostrar_c(Toplevel(self.window)))
        #self.cascada.add_command(label='Buscar Cliente',
        #            command=lambda: self.ventana_buscar_c(Toplevel(self.window)))
        self.cascada.add_command(label='Agregar Cliente',
                    command=lambda: self.ventana_agregar_c(Toplevel(self.window)))
        self.cascada2 = Menu(self.menus,tearoff=0)
        self.cascada2.add_command(label='Cambiar Nombre',
                    command=lambda: self.ventana_editar_nombre(Toplevel(self.window)))
        self.cascada2.add_command(label='Cambiar Contraseña',
                    command=lambda: self.ventana_editar_pw(Toplevel(self.window)))
        self.menus.add_cascade(label='Clientes',state='disabled', menu=self.cascada)
        self.menus.add_command(label='Crear Usuario',state='disabled',
                    command=lambda: self.ventana_nuevo_usuario(Toplevel(self.window)))
        self.menus.add_cascade(label='Editar Usuario',state='disabled', menu=self.cascada2)
        self.menus.add_command(label='Cerrar Sesión',state='disabled',
                               command = self.cerrar_sesion)

        self.window.config(menu=self.menus) 

        self.window.resizable(False, False)
        
    def activar_todo(self):          
        messagebox.showinfo('Bienvenido','Sesión iniciada con éxito')
        self.menus.entryconfig('Iniciar Sesión',state='disabled')
        self.menus.entryconfig("Crear Usuario",state='normal')
        self.menus.entryconfig("Editar Usuario",state='normal')
        self.menus.entryconfig("Clientes",state='normal')
        self.menus.entryconfig("Cerrar Sesión",state='normal')
        self.menus.entryconfig("Estado General",state='normal')
        self.cargar_obras()
        self.actualizar_valores()
    
    def cargar_obras(self):
        vals = sql.select_all_obras()
        self.combo['values'] = vals
        try:
            self.combo.current(0)
            self.lbljaja["text"]= self.combo.get()
        except:
            pass
        self.btn2.state(['!disabled'])
        self.btn1.state(['!disabled'])
        self.btn3.state(['!disabled'])
        self.btn4.state(['!disabled'])
        self.btn5.state(['!disabled'])
        self.btn6.state(['!disabled'])
        self.btn7.state(['!disabled'])
        self.btn8.state(['!disabled'])
        self.btn.state(['!disabled'])
       
        
    def actualizar_valoress(self,machete):
        self.actualizar_valores()
    
    def actualizar_valores(self):
        name = self.combo.get()
        self.actual_obra = name.split(".")[0].replace('.','')
        texto = self.txt
        try:

            obra = sql.get_obra(self.combo.get().split(".")[0])
            self.lbljaja["text"]= self.combo.get() + '\n'+\
                'Ciudad: ' + obra[2] + '\nDirección: ' + obra[3]
        except:
            pass
        corpus = ''
      
        corpus = name
        
        try:
            trans = sql.select_transacciones_obra(self.actual_obra)
            rubs = sql.select_rubros_obra(self.actual_obra)
        except:
            return
        
        synth = self.analizar_transacciones(trans,rubs)
        estado = [0,0,0]
        rc = {"Antes":[],"Durante":[],"Después":[]}
        estado2 = {"Antes":[0,0],"Durante":[0,0],"Después":[0,0]}
        for rub in rubs:
            estado[2]+=rub[4]
            if rub[3] != "Entrada":
                rc[rub[3]].append(rub[0])
                estado2[rub[3]][0]+=rub[4]
        for tran in trans:
            if tran[5]=="Entrada":
                estado[0]+=tran[4]
            elif tran[5]=="Salida":
                estado[1]+=tran[4]
                if tran[3] in rc["Antes"]:
                    estado2["Antes"][1]+=tran[4]
                elif tran[3] in rc["Durante"]:
                    estado2["Durante"][1]+=tran[4]
                elif tran[3] in rc["Después"]:
                    estado2["Después"][1]+=tran[4]
                

    
        for val in synth:
            gen = ''
            if val == "EGRESOS":
                gen = '\tPresupuesto: '+str(estado[2])+ '\t Gastos:' + str(estado[1])
            else:
                gen = str(estado[0])
            corpus+= '\n----------------------------------------------------------------------'
            corpus+= '\t   '+val+ ' $' +  gen
            corpus+= '\n----------------------------------------------------------------------'
            dummy = synth[val]
            if val == "INGRESOS":
                for damn in dummy:
                    corpus+= '\n'
                    corpus+= damn
                    corpus+=':  \t'
                    corpus+= str(dummy[damn])
            if val == "EGRESOS":
                for goddamn in dummy:
                    gen = '\tPresupuesto: '+str(estado2[goddamn][0])+ '\t Gastos:' + str(estado2[goddamn][1])
                    corpus+= '\n----------------------------------------------------------------------'
                    corpus+= '\t    '+goddamn+ ' $'+gen
                    corpus+= '\n----------------------------------------------------------------------' 
                    for porfin in dummy[goddamn]:
                        corpus+= '\n'
                        corpus+= porfin
                        corpus+=':  \t'
                        corpus+='P: '
                        corpus+= str(dummy[goddamn][porfin][0])
                        corpus+='\tG: '
                        corpus+= str(dummy[goddamn][porfin][1])               

        texto.delete(1.0,END)
        texto.insert(INSERT,corpus)
        
        fig = plt.figure(figsize=(4.7,2.5))
        
        objects = ('Ingresos','Gasto','Presupuesto')
        y_pos = np.arange(len(objects))
        
        plt.bar(y_pos, estado, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('$')
        plt.title('Estado de la Obra')
        
        self.labeljiji = FigureCanvasTkAgg(fig, master=self.window)  # A tk.DrawingArea.
        self.labeljiji.draw()
        self.labeljiji.get_tk_widget().grid(column=0, row=1, sticky =(S))
        
    
    def analizar_transacciones(self,listat,listar):
        
        
        xd = {"INGRESOS":{},
              "EGRESOS":{
                      "Antes":{},
                      "Durante":{},
                      "Después":{}
                      }}
        for j in listar:
            if j[3] == "Entrada":
                xd['INGRESOS'][j[2]] = 0
                for i in listat:
                    if j[0] == i[3]:
                        xd['INGRESOS'][j[2]]+=i[4]
            else:
                xd['EGRESOS'][j[3]][j[2]] = [j[4],0]
                for i in listat:
                    if j[0] == i[3]:
                        xd['EGRESOS'][j[3]][j[2]][1]+=i[4]

        return xd
            
    def agregar_obr(self,nm,ct,dr,ie,fim,fid,fia,fcm,fcd,fca,cerlib,lic,info):
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
            messagebox.showerror('Error', 'Las fechas no son válidas')
            return False
        elif fat:
            messagebox.showerror('Error', 'La Obra no puede empezar después de terminar')
            return False
        if nm.strip() == '' or ct.strip() == '' or dr.strip() == '':
            messagebox.showerror('Error', 'La obra no puede registrarse con nombre, ciudad o dirección vacíos')
            return False
        fi = str(fid) + '-' + str(yd[fim]) + "-" + str(fia)
        fc = str(fcd) + '-' + str(yd[fcm]) + "-" + str(fca)
        try:
            helper = sql.create_obra((nm,ct,dr,ie,fi,fc,cerlib,lic,0,info))
            messagebox.showinfo('Crear Obra','Obra creada con éxito')
            self.rubros_por_defecto(helper)
            #TODO RUBROS DEFECTO

        except:
            messagebox.showerror('Error','La obra no pudo ser creada')
            return False
        self.cargar_obras()
        self.actualizar_valores()
        return True
    
    def rubros_por_defecto(self,helper):
        sql.create_rubro((helper,"Inversionistas","Entrada",0))
        sql.create_rubro((helper,"Ventas","Entrada",0))
        sql.create_rubro((helper,"Préstamos","Entrada",0))
        sql.create_rubro((helper,"Planos","Durante",0))
        sql.create_rubro((helper,"Retorno Inversionistas","Después",0))
        #TODO Diversificar rubros de entrada
        
    def validar_fecha(m,d,a):
        isValidDate = True
        try :
            datetime.datetime(a,m,d)
        except ValueError :
            isValidDate = False
        return isValidDate
    
    def agregar_rub(self,nombre,tipo,valor):
        
        nombre = nombre.replace(":","")
        hue = sql.select_rubros_obra(self.actual_obra)
        
        for fact in hue:
            if nombre == fact[2]:
                messagebox.showerror('Error','El rubro ya existe')
                return
        sql.create_rubro((self.actual_obra,
                                    nombre,
                                    tipo,
                                    valor))
        messagebox.showinfo('Crear Rubro','Rubro creado con éxito')
        self.actualizar_valores()

    
    def agregar_transac(self,nombre,valor):
        
        hue = sql.select_transacciones_obra(self.actual_obra)
        
        verify = nombre.split(": ")[0]
        realname = nombre.split(": ")[1]
        
        asociador = sql.get_rubro_by_nombre_obra((realname,self.actual_obra))
        
        if verify == "Entrada":
            sql.create_transaccion((self.actual_obra,
                                    self.actual_user,
                                    asociador,
                                    valor,
                                    'Entrada'
                                    ))
            messagebox.showinfo('Crear Transacción','Transacción creada con éxito')
            self.actualizar_valores()
        else:
            sepuede = self.verificar_dinero(hue,valor)
            if sepuede:
                sql.create_transaccion((self.actual_obra,
                                    self.actual_user,
                                    asociador,
                                    valor,
                                    'Salida'
                                    ))            
                messagebox.showinfo('Registrar Transacción','Transacción realizada con éxito')
                self.actualizar_valores()
            else:
                messagebox.showerror('Error','La transacción excede el dinero disponible')
    
    def cambiar_presupuesto(self,nombre,valor):
        
        realname = nombre.split(": ")[1]
        
        asociador = sql.get_rubro_by_nombre_obra((realname,self.actual_obra))
        sql.update_presupuesto_rubro(valor,asociador)
        self.actualizar_valores()
        messagebox.showinfo('Presupuesto','El presupuesto se actualizó con éxito')
        
    def editar_obra(self,nombre,valor):
        
        translate = {'Nombre':'nombre',
                     'Ciudad':'ciudad',
                     'Dirección':'direccion',
                     'Encargado':'encargado',
                     'Certificado Libertad':'cer_lib',
                     'Licencia de Construccion':'licencia', 
                     'Apartamentos Disponibles':'disponibles',
                     'Información Adicional':'info_extra'}
        if translate[nombre] == "disponibles":
            try:
                elvalor = valor.get().strip()
                if elvalor == '':
                    elvalor = 0
                valor = float(elvalor)
            except:
                messagebox.showerror('Error', 'Ingrese un valor numerico para el nuevo Presupuesto')
                return False
        sql.update_obra((translate[nombre],valor,self.actual_obra))
        self.cargar_obras()
        self.actualizar_valores()
        messagebox.showinfo('Presupuesto','El presupuesto se actualizó con éxito')
        return True
        
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
        
        if self.master != None:
            self.master.destroy()
        
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
        
    #Ventana Estado General
    
    def ventana_estadogeneral(self,master):

        if self.master != None:
            self.master.destroy()        
        
        self.master = master
        self.master.geometry("820x320")
        self.frame = Frame(self.master)
        
        def close_window(self):
            self.master.destroy()
            
        data = self.generar_estado(sql.select_all_obras())
            
        self.quit = Button(self.frame, text = " Cancelar ", 
                           command = lambda : close_window(self))
        self.lbltt = Label(self.frame,text="Presupuesto General",font=("Arial",14))
        self.lblio = Label(self.frame,text="Ingresos: $"+str(data[0][0])+
                           "   Egresos: $"+str(data[0][1]),font=("Arial",14)) 
        
        self.vista = Treeview(self.frame, columns = ("entrada", "presupuesto","gasto"))
        
        self.vsb = Scrollbar(self.frame, orient="vertical", command=self.vista.yview)
        self.vsb.pack(side='right', fill='y')
        self.vista.configure(yscrollcommand=self.vsb.set)
        
        self.vista.heading("#0", text="Obra")
        self.vista.heading("entrada", text="Entrada")
        self.vista.heading("presupuesto", text="Presupuesto")
        self.vista.heading("gasto", text="Gasto")
        
        for i in range(1,len(data)):
            self.vista.insert("",END,text=data[i][0],values=(data[i][1],
                              data[i][2],
                              data[i][3]))
        self.lbltt.pack()
        self.lblio.pack()
        self.vista.pack()       
        self.quit.pack()
        self.master.resizable(False, False)
        self.frame.pack()
    
    def generar_estado(self,lista_obras):
        estado = []
        estado.append([0,0])
        for i in range(len(lista_obras)):
            mock = lista_obras[i].split(". ")
            temp = sql.select_transacciones_obra(mock[0])
            temp2 = sql.select_rubros_obra(mock[0])
            estado.append([lista_obras[i],0,0,0])
            for trans in temp:
                if trans[5]=="Entrada":
                    estado[0][0]+=trans[4]
                    estado[i+1][1]+=trans[4]
                elif trans[5]=="Salida":
                    estado[0][1]+=trans[4]
                    estado[i+1][3]+=trans[4]                    
            for rub in temp2:
                estado[i+1][2]+=rub[4]
        return estado
    
    #Ventana info Obra
    
    def ventana_info_obra(self,master):
        
        if self.master != None:
            self.master.destroy()
            
        self.master = master
        self.master.geometry("370x240")
        self.frame = Frame(self.master)
        
        def close_window(self):
            self.master.destroy()
            
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))       
        
        data = sql.get_obra(self.actual_obra)
        
        if len(data) ==0:
            self.lblerr = Label(self.frame,text="No hay obras \n disponibles",font=("Arial",14))
            self.lblerr.pack()
            self.quit.pack()
            self.master.resizable(False, False)
            self.frame.pack()  
        else:
            self.lblp = Label(self.frame,text=data[1],font=("Arial",14))
            self.lblq = Label(self.frame,text="Ciudad: "+data[2],font=("Arial",12))
            self.lblr = Label(self.frame,text="Direccion: "+data[3],font=("Arial",12))
            self.lbls = Label(self.frame,text="Ingeniero Encargado: "+data[4],font=("Arial",12))
            self.lblcl = Label(self.frame,text="Certificado Libertad: "+data[7],font=("Arial",12))
            self.lbllic = Label(self.frame,text="Licencia: "+data[8],font=("Arial",12))
            self.lblu = Label(self.frame,text="Apartamentos Disponibles: "+str(data[9]),font=("Arial",12))
            self.lblt = Label(self.frame,text="Fecha Inicio: "+data[5]+" Fecha Culminación: "
                          +data[6],font=("Arial",11))

            temp = sql.select_transacciones_obra(self.actual_obra)
            temp2 = sql.select_rubros_obra(self.actual_obra)
            estado = [0,0,0]
            for trans in temp:
                if trans[5]=="Entrada":
                    estado[0]+=trans[4]
                elif trans[5]=="Salida":
                    estado[1]+=trans[4]                    
            for rub in temp2:
                estado[2]+=rub[4]
            self.lblest = Label(self.frame,text = "Presupuesto: $" +
                                str(estado[2])+ "\nEntradas: $" +
                                str(estado[0])+ "\nSalidas: $" +
                                str(estado[1]),font=("Arial",12))    
            
            self.lblp.pack()
            self.lblq.pack()
            self.lblr.pack()
            self.lbls.pack()
            self.lblcl.pack()
            self.lbllic.pack()
            self.lblu.pack()
            self.lblt.pack()
            self.lblest.pack()
            self.quit.pack()
            self.master.resizable(False, False)
            self.frame.pack()    
        
    #Ventana para Agregar Usuario
    def ventana_nuevo_usuario(self,master):
        
        if self.master != None:
            self.master.destroy()
        
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
    
    #Ventana Editar Nombre
    def ventana_editar_nombre(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x170")
        self.frame = Frame(self.master)
         
        def close_window(self):
            self.master.destroy()
        
        def editar_el_nuser(n1,n2):
            if n1.get()!= n2.get():
                messagebox.showerror('Error', 'Los nuevos nombres deben coincidir')
            else:
                sql.update_nuser(self.actual_user,n1.get())
                messagebox.showinfo('Éxito','Se ha modificado su nombre')
            self.master.destroy()
        self.quit = Button(self.frame, text = " Cancelar ", 
                           command = lambda : close_window(self))
        thename = sql.get_name_by_user(self.actual_user)
        self.actn = Label(self.frame,text = thename,font=("Arial",12))
        self.lblnn = Label(self.frame,text="Nuevo Nombre",font=("Arial",10))
        self.entrnn = Entry(self.frame,width=35)
        self.lblnn2 = Label(self.frame,text="Confirme nuevo Nombre",font=("Arial",10))
        self.entrnn2 = Entry(self.frame,width=35)
        self.blank = Label(self.frame,text=" ")
        self.agregar = Button(self.frame, text = "Cambiar", 
                              command = lambda: editar_el_nuser(self.entrnn,
                                                                self.entrnn2))
        self.actn.pack()
        self.lblnn.pack()
        self.entrnn.pack()
        self.lblnn2.pack()
        self.entrnn2.pack()
        self.blank.pack()
        self.quit.pack(side = "left")
        self.agregar.pack(side = "right")
        self.master.resizable(False, False)
        self.frame.pack()
        
    #Ventana Editar Contraseña
    def ventana_editar_pw(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x140")
        self.frame = Frame(self.master)
         
        def close_window(self):
            self.master.destroy()
        
        def editar_el_puser(p1,p2):
            if p1.get()!= p2.get():
                messagebox.showerror('Error', 'Las nuevas contraseñas deben coincidir')
            else:
                sql.update_puser(self.actual_user,p1.get())
                messagebox.showinfo('Éxito','Se ha modificado su contraseña')
            self.master.destroy()
        self.quit = Button(self.frame, text = " Cancelar ", 
                           command = lambda : close_window(self))
        self.lblp = Label(self.frame,text="Nueva Contraseña",font=("Arial",10))
        self.entrp = Entry(self.frame,show="*",width=35)
        self.lblp2 = Label(self.frame,text="Confirme nuevo Nombre",font=("Arial",10))
        self.entrp2 = Entry(self.frame,show="*",width=35)
        self.blank = Label(self.frame,text=" ")
        self.agregar = Button(self.frame, text = "Cambiar", 
                              command = lambda: editar_el_puser(self.entrp,
                                                                self.entrp2))
        self.lblp.pack()
        self.entrp.pack()
        self.lblp2.pack()
        self.entrp2.pack()
        self.blank.pack()
        self.quit.pack(side = "left")
        self.agregar.pack(side = "right")
        self.master.resizable(False, False)
        self.frame.pack()
    
    #Ventana Ver Clientes
    def ventana_mostrar_c(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("620x260")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()      
        
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        self.vista = Treeview(self.frame, columns = ("td", "id"))
        self.vsb = Scrollbar(self.frame, orient="vertical", command=self.vista.yview)
        self.vsb.pack(side='right', fill='y')
        self.vista.configure(yscrollcommand=self.vsb.set)
        
        self.vista.heading("#0", text="Nombre")
        self.vista.heading("td", text="Tipo de Documento")
        self.vista.heading("id", text="Documento")

        cl = sql.select_all_clientes()
        for i in cl:
            self.vista.insert("",END,text=i[0],values=(i[1],i[2]))
        self.vista.pack()
        self.quit.pack()
        self.master.resizable(False, False)
        self.frame.pack()
    
    #Ventana Buscar Cliente
    def ventana_buscar_c(self,master):
            
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("620x300")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()      
        def actualizar():
            pass
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        
        
    
    #Ventana Agregar Clientes
    def ventana_agregar_c(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x320")
        self.frame = Frame(self.master)
         
        def close_window(self):
            self.master.destroy()
        
        def agregar_el_cliente(n,td,doc,ce,tel,dirc):
            trial = sql.select_all_clientes()
            docs = []
            for i in trial:
                docs.append(i[2])
            if doc.get() in docs:
                messagebox.showerror('Error', 'Ya existe un cliente con este documento')
            elif n.get() == '' or td.get() == '' or doc.get() == '' :
                messagebox.showerror('Error', 'El nombre y documento no deben ser vacíos')
            else:
                sql.create_cliente((n.get(),td.get(),doc.get(),ce.get(),tel.get(),dirc.get()))
                messagebox.showinfo('Éxito','Se ha agregado el cliente')
                self.master.destroy()
        self.quit = Button(self.frame, text = " Cancelar ", 
                           command = lambda : close_window(self))
        self.lbltit = Label(self.frame,text="Ingrese los Datos",font=("Arial",12))
        self.lbln = Label(self.frame,text="Nombre",font=("Arial",10))
        self.entrn = Entry(self.frame,width=35)
        self.lbltd = Label(self.frame,text="Tipo de Documento",font=("Arial",10))
        self.entrtd = Entry(self.frame,width=35)
        self.lbld = Label(self.frame,text="Documento",font=("Arial",10))
        self.entrd = Entry(self.frame,width=35)
        self.lblce = Label(self.frame,text="Correo Electrónico",font=("Arial",10))
        self.entrce = Entry(self.frame,width=35)
        self.lblt = Label(self.frame,text="Teléfono",font=("Arial",10))
        self.entrt = Entry(self.frame,width=35)
        self.lbltdr = Label(self.frame,text="Dirección",font=("Arial",10))
        self.entrtdr = Entry(self.frame,width=35)
        self.blank = Label(self.frame,text=" ")
        self.agregar = Button(self.frame, text = "Registrar", 
                              command = lambda: agregar_el_cliente(self.entrn,
                                                                self.entrtd,
                                                                self.entrd,
                                                                self.entrce,
                                                                self.entrt,
                                                                self.entrtdr))
        self.lbltit.pack()
        self.lbln.pack()
        self.entrn.pack()
        self.lbltd.pack()
        self.entrtd.pack()
        self.lbld.pack()
        self.entrd.pack()
        self.lblce.pack()
        self.entrce.pack()
        self.lblt.pack()
        self.entrt.pack()
        self.lbltdr.pack()
        self.entrtdr.pack()
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
            self.menus.entryconfig("Editar Usuario",state='disabled')
            self.menus.entryconfig("Estado General",state='disabled')
            self.menus.entryconfig("Clientes",state='disabled')
            self.actual_user = ''
            self.actual_obra = 0
            self.txt.delete(1.0,END)
            self.combo['values'] = ()
            self.combo.delete(0,END)
            self.btn2.state(['disabled'])
            self.btn1.state(['disabled'])
            self.btn.state(['disabled'])
            self.btn3.state(['disabled'])
            self.btn4.state(['disabled'])
            self.btn5.state(['disabled'])
            self.btn6.state(['disabled'])
            self.btn7.state(['disabled'])
            self.btn8.state(['disabled'])
            self.lbljaja["text"]=''
            if self.master != None:
                self.master.destroy()
            
            
    #Ventana para Agregar Obra
    
    def ventana_agregar_o(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x435")
        self.frame = Frame(self.master)
          
        def close_window(self):
            self.master.destroy()
        
        def agregar_la_obra(self,nm,ct,dr,ie,fim,fid,fia,fcm,fcd,fca,crlib,licon,info):
            sepudo = main.agregar_obr(self,nm.get(),
                             ct.get(),
                             dr.get(),
                             ie.get(),
                             fim.get(),
                             fid.get(),
                             fia.get(),
                             fcm.get(),
                             fcd.get(),
                             fca.get(),
                             crlib.get(),
                             licon.get(),
                             info.get())
            if sepudo:
                self.master.destroy()
            
        self.quit = Button(self.frame, text = " Salir ",
                           command = lambda : close_window(self))
        self.lbla = Label(self.frame,text="Nombre de la Obra",font=("Arial",10))
        self.entra = Entry(self.frame,width=35)
        self.lblb = Label(self.frame,text="Ciudad",font=("Arial",10))
        self.entrb = Entry(self.frame,width=35)
        self.lblc = Label(self.frame,text="Dirección",font=("Arial",10))
        self.entrc = Entry(self.frame,width=35)
        self.lbld = Label(self.frame,text="Encargado",font=("Arial",10))
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
        self.lblg = Label(self.frame,text="Certificado de Libertad",font=("Arial",10))
        self.entrg = Entry(self.frame,width=35)
        self.lblh = Label(self.frame,text="Licencia de Construcción",font=("Arial",10))
        self.entrh = Entry(self.frame,width=35)
        self.lbli = Label(self.frame,text="Información Adicional",font=("Arial",10))
        self.entri = Entry(self.frame,width=35)
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
                                                                self.combf3,
                                                                self.entrg,
                                                                self.entrh,
                                                                self.entri)) 
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
        self.lblg.grid(column=0,row=12)
        self.entrg.grid(column=0,row=13)
        self.lblh.grid(column=0,row=14)
        self.entrh.grid(column=0,row=15)
        self.lbli.grid(column=0,row=16)
        self.entri.grid(column=0,row=17)
        self.blank.grid(column=0,row=18)
        self.quit.grid(column=0,row=19, sticky = (W))
        self.agregar.grid(column=0,row=19, sticky = (E))
        self.master.resizable(False, False)
        self.frame.pack()        
    
    #Ventana para Agregar Rubro
    
    def ventana_agregar_r(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x200")
        self.frame = Frame(self.master)
        self.huh = IntVar()
          
        def close_window(self):
            self.master.destroy()      
        
        def agregar_el_rubro(self,nombre,valor,tipo):
            
            if nombre.get().strip() == '':            
                messagebox.showerror('Error', 'Ingrese un nombre válido para el rubro') 
            try:
                elvalor = valor.get().strip()
                if elvalor == '':
                    elvalor = 0
                float(elvalor)
                main.agregar_rub(self,
                                 nombre.get(),
                                 tipo.get(),
                                 float(elvalor))
                self.master.destroy()
            except:
                messagebox.showerror('Error', 'Ingrese un valor númerico para el valor del rubro')      
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        if self.actual_obra == '':
            self.lblerr = Label(self.frame,text="No hay obras \n disponibles",font=("Arial",14))
            self.lblerr.pack()
            self.quit.pack()
            self.master.resizable(False, False)
            self.frame.pack()  
        
        else:
            self.lblm = Label(self.frame,text="Ingrese Nombre del Rubro",font=("Arial",10))
            self.entrm = Entry(self.frame,width=35)
            self.lbln = Label(self.frame,text="Ingrese Presupuesto",font=("Arial",10))
            self.entrn = Entry(self.frame,width=35)
            self.lblti = Label(self.frame,text="Seleccione Tipo Rubro",font=("Arial",10))
            self.blank = Label(self.frame,text=" ",font=("Arial",10))
            self.combru = Combobox(self.frame,width=32)
            self.combru['values'] = ("Antes","Durante","Después")
            self.combru.current(0)
            self.agregar = Button(self.frame, text = "Agregar",
                              command = lambda: agregar_el_rubro(self,
                                                                 self.entrm,
                                                                 self.entrn,
                                                                 self.combru))
            self.lblm.pack()
            self.entrm.pack()
            self.lbln.pack()
            self.entrn.pack()
            self.lblti.pack()
            self.combru.pack()
            self.blank.pack()
            self.quit.pack(side = "left")
            self.agregar.pack(side = "right")
            self.master.resizable(False, False)
            self.frame.pack()

    
    #Ventana para Agregar Transacción
    def ventana_agregar_t(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x150")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()      
        
        def agregar_trans(self,nombre,valor):
            try:
                elvalor = valor.get().strip()
                if elvalor == '':
                    elvalor = 0
                float(elvalor)
                main.agregar_transac(self,
                                 nombre.get(),
                                 float(elvalor))
                self.master.destroy()
            except:
                messagebox.showerror('Error', 'Ingrese un valor númerico para el valor de la transacción') 
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        
        if self.actual_obra == '':
            self.lblerr = Label(self.frame,text="No hay obras \n disponibles",font=("Arial",14))
            self.lblerr.pack()
            self.quit.pack()
            self.master.resizable(False, False)
            self.frame.pack()  
        
        else:
        
            self.lbly = Label(self.frame,text="Seleccionar Rubro",font=("Arial",10))
            self.cbb = Combobox(self.frame,width=32)
            self.cbb['values'] = sql.get_rubros_obra(self.actual_obra)
            self.cbb.current(0)
            self.lblu = Label(self.frame,text="Ingrese Nueva Transacción",font=("Arial",10))
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
       
    #Ventana cambiar presupuesto    
    def ventana_editar_p(self,master):
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x150")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()  
            
        def quitar_entradas(lista):
            lista1 = []
            for i in lista:
                if i.split(": ")[0] != "Entrada":
                    lista1.append(i)
            return lista1
        
        def cam_presu(self,nombre,valor):
            try:
                elvalor = valor.get().strip()
                if elvalor == '':
                    elvalor = 0
                float(elvalor)
                main.cambiar_presupuesto(self,
                                 nombre.get(),
                                 float(elvalor))
                self.master.destroy()
            except:
                messagebox.showerror('Error', 'Ingrese un valor númerico para el nuevo Presupuesto') 
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        
        if self.actual_obra == '':
            self.lblerr = Label(self.frame,text="No hay obras \n disponibles",font=("Arial",14))
            self.lblerr.pack()
            self.quit.pack()
            self.master.resizable(False, False)
            self.frame.pack()  
        
        else:
        
            self.lbly = Label(self.frame,text="Seleccionar Rubro",font=("Arial",10))
            self.cbb = Combobox(self.frame,width=32)
            self.cbb['values'] = quitar_entradas(sql.get_rubros_obra(self.actual_obra))
            self.cbb.current(0)
            self.lblu = Label(self.frame,text="Ingrese Nuevo Presupuesto",font=("Arial",10))
            self.entru = Entry(self.frame,width=35)
            self.agregar = Button(self.frame, text = "Editar", 
                              command = lambda: cam_presu(self,
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
    
    #Ventana editar obra
    def ventana_editar_o(self,master):
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x150")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()  
        
        def cam_obr(self,nombre,valor):
            if  main.editar_obra(self,
                                 nombre.get(),
                                 valor.get()) :
                self.master.destroy() 
        self.quit = Button(self.frame, text = " Cancelar ", 
                           command = lambda : close_window(self))
        
        if self.actual_obra == '':
            self.lblerr = Label(self.frame,text="No hay obras \n disponibles",font=("Arial",14))
            self.lblerr.pack()
            self.quit.pack()
            self.master.resizable(False, False)
            self.frame.pack()  
        
        else:
        
            self.lbly = Label(self.frame,text="Seleccionar elemento",font=("Arial",10))
            self.cbb = Combobox(self.frame,width=32)
            self.cbb['values'] = ('Nombre','Ciudad','Dirección'
                                'Encargado','Certificado Libertad',
                                'Licencia de Construccion', 'Apartamentos Disponibles',
                                'Información Adicional')
            self.cbb.current(0)
            self.lblu = Label(self.frame,text="Ingrese Nuevo Valor",font=("Arial",10))
            self.entru = Entry(self.frame,width=35)
            self.agregar = Button(self.frame, text = "Aceptar", 
                              command = lambda: cam_obr(self,
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
    def ventana_mostrar_f(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("1030x260")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()      
        
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        self.vista = Treeview(self.frame, columns = ("rubro", "tipo","valor","responsable"))
        self.vsb = Scrollbar(self.frame, orient="vertical", command=self.vista.yview)
        self.vsb.pack(side='right', fill='y')
        self.vista.configure(yscrollcommand=self.vsb.set)
        
        self.vista.heading("#0", text="ID")
        self.vista.heading("rubro", text="Rubro")
        self.vista.heading("tipo", text="Tipo Transacción")
        self.vista.heading("valor", text="Valor")
        self.vista.heading("responsable", text="Responsable")
        
        if self.actual_obra == '': 
            tr = []
        else:
            tr = sql.select_transacciones_obra(self.actual_obra)
        for i in tr:

            nombre = sql.get_nombre_rubro((i[3],))

            self.vista.insert("",END,text=i[0],values=(nombre,
                              i[5],
                              i[4],
                              sql.get_name_by_user(i[2])))
        self.vista.pack()
        self.quit.pack()
        self.master.resizable(False, False)
        self.frame.pack()
                                   
    #Ventana para ver graficas de obra
    
    def  ver_graficas(self,master):
        if self.master != None:
            self.master.destroy()
        self.master = master
        self.frame = Frame(self.master)
                    
        trans = sql.select_transacciones_obra(self.actual_obra)
        rubs = sql.select_rubros_obra(self.actual_obra)
        
        synth = self.analizar_transacciones(trans,rubs)
        
        
        
        def graph_1():
            
            self.labelji = ''
            fig1 = plt.figure(figsize=(6,5))
            plt.clf()
            fig1 = plt.figure(figsize=(6,5))
            labels=list(synth["INGRESOS"].keys())
            sizes=list(synth["INGRESOS"].values())
            colors = ['gold', 'lightcoral', 'lightskyblue']
    
        
            plt.pie(sizes, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=140)

            plt.axis('equal')
            plt.title('Repartición de Ingresos')

            self.labelji = FigureCanvasTkAgg(fig1, master=self.master)  # A tk.DrawingArea.
            self.labelji.draw()
            self.labelji.get_tk_widget().grid(column=0, row=0)
            
        def graph_2():
            
            self.labeljii = ''
            fig = plt.figure(figsize=(6,5))
            plt.clf()
            estado = [0,0,0]
            rc = {"Antes":[],"Durante":[],"Después":[]}
            estado2 = {"Antes":[0,0],"Durante":[0,0],"Después":[0,0]}
            for rub in rubs:
                estado[2]+=rub[4]
                if rub[3] != "Entrada":
                    rc[rub[3]].append(rub[0])
                    estado2[rub[3]][0]+=rub[4]
            for tran in trans:
                if tran[5]=="Entrada":
                    estado[0]+=tran[4]
                elif tran[5]=="Salida":
                    estado[1]+=tran[4]
                    if tran[3] in rc["Antes"]:
                        estado2["Antes"][1]+=tran[4]
                    elif tran[3] in rc["Durante"]:
                        estado2["Durante"][1]+=tran[4]
                    elif tran[3] in rc["Después"]:
                        estado2["Después"][1]+=tran[4]
            
            n_groups = 3
            presupuestos = (estado2["Antes"][0], estado2["Durante"][0], estado2["Después"][0])
            gastos = (estado2["Antes"][1], estado2["Durante"][1], estado2["Después"][1])

            fig, ax = plt.subplots()
            index = np.arange(n_groups)
            bar_width = 0.35
            opacity = 0.8

            rects1 = plt.bar(index, presupuestos, bar_width,
                             alpha=opacity,
                             color='b',
                             label='Presupuesto')

            rects2 = plt.bar(index + bar_width, gastos, bar_width,
                             alpha=opacity,
                             color='r',
                             label='Gastos')

            plt.xlabel('Person')
            plt.ylabel('Dinero')
            plt.title('Presupuesto vs Gastos')
            plt.xticks(index + bar_width, ('A', 'B', 'C', 'D'))
            plt.legend()
            
            plt.tight_layout()
            
            self.labeljii = FigureCanvasTkAgg(fig, master=self.master)  # A tk.DrawingArea.
            self.labeljii.draw()
            self.labeljii.get_tk_widget().grid(column=0, row=1)


        def _quit():
                    # stops mainloop
            self.master.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        if self.actual_obra != '':
            graph_1()
            graph_2()
        
        self.buttoon = Button(self.frame, text="Salir", command=_quit)
        self.buttoon.grid(column=0, row=2, sticky =(W))
        self.master.resizable(False, False)
        #self.frame.pack()
   
    

root = Tk()
app = main(root)
root.mainloop()
