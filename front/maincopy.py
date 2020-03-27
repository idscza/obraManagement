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

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np



class main:
    def __init__(self,window):
        
        self.master = None
        self.minaster = None
        self.window = window
        self.window.title("Manejo de Obras")
        self.window.geometry('1270x660')
        
        self.actual_user = StringVar()
        self.actual_obra = IntVar()
        self.sudo = BooleanVar()
        self.quotes = []

        self.lbljaja = Label(window, text="",font=("Arial",11))
        self.lbljaja.grid(column=0, row=1, sticky =(N))
        
        self.lbljiji = Label(window, text="",font=("Arial",12))
        self.lbljiji.grid(column=0, row=1, sticky =(S))

        
        self.photo = Image.open("pic.png")
        self.thephoto = ImageTk.PhotoImage(self.photo)
        self.lbl = Label(window,image=self.thephoto)
        self.lbl.grid(column=0, row=1)
        self.lbl.image = self.thephoto

        self.lbl1 = Label(window, text=' ')
        self.lbl1.grid(column=1,row=0)
    
        self.lbl2 = Label(window, text='         ')
        self.lbl2.grid(column=1,row=1)
    
        self.txt = scrolledtext.ScrolledText(window,width=110,height=35)
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
        
        
        self.btn3 = Button(window, text="Mostrar Transacciones",
                           command = lambda: self.ventana_mostrar_f(Toplevel(self.window)),
                           state='disabled')
        self.btn3.grid(column=2, row=2, sticky = (E))
    
        self.btn2 = Button(window, text="Registrar Transacción",
                           command=lambda: self.ventana_agregar_t(Toplevel(self.window))
                               ,state='disabled')
        self.btn2.grid(column=2, row=2)
        
        self.btn4 = Button(window, text="  Registrar Contrato  ",
                           command=lambda: self.ventana_agregar_cont(Toplevel(self.window))
                               ,state='disabled')
        self.btn4.grid(column=2, row=3)
        
        self.btn5 = Button(window, text="Información Obra        ",
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
        self.cascada.add_command(label='Info Cliente',
                    command=lambda: self.ventana_buscar_c(Toplevel(self.window)))
        self.cascada.add_command(label='Agregar Cliente',state='disabled',
                    command=lambda: self.ventana_agregar_c(Toplevel(self.window)))
        self.cascada2 = Menu(self.menus,tearoff=0)
        self.cascada2.add_command(label='Cambiar Nombre',
                    command=lambda: self.ventana_editar_nombre(Toplevel(self.window)))
        self.cascada2.add_command(label='Cambiar Contraseña',
                    command=lambda: self.ventana_editar_pw(Toplevel(self.window)))
        self.menus.add_cascade(label='Clientes',state='disabled', menu=self.cascada)
        self.menus.add_command(label='Ver Cobros Semana',state='disabled',
                    command=lambda: self.mostrar_facturas_pendientes(Toplevel(self.window)))
        self.menus.add_command(label='Pagar Cuentas',state='disabled',
                    command=lambda: self.ventana_pagar_cuentas(Toplevel(self.window)))
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
        self.menus.entryconfig("Ver Cobros Semana",state='normal')
        self.menus.entryconfig("Clientes",state='normal')
        if self.sudo:
            self.cascada.entryconfig('Agregar Cliente',state='normal')
            self.menus.entryconfig("Pagar Cuentas",state='normal')
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
        if self.sudo:
            self.btn7.state(['!disabled'])
            self.btn8.state(['!disabled'])
            self.btn.state(['!disabled'])
            self.btn2.state(['!disabled'])
            self.btn1.state(['!disabled'])
            self.btn4.state(['!disabled'])
        self.btn3.state(['!disabled'])
        self.btn5.state(['!disabled'])
        self.btn6.state(['!disabled'])

       
        
    def actualizar_valoress(self,machete):
        self.actualizar_valores()
    
    def actualizar_valores(self):
        name = self.combo.get()
        self.actual_obra = name.split(".")[0].replace('.','')
        texto = self.txt

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
            corpus+= '\n----------------------------------------------------------------------'+\
                '---------------------------------------\n'
            corpus+= '\t   '+val+ ' $' +  gen
            corpus+= '\n----------------------------------------------------------------------'+\
                '---------------------------------------'
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
                    corpus+=  '\n----------------------------------------------------------------------'+\
                '---------------------------------------\n'
                    corpus+= '\t    '+goddamn+ ' $'+gen
                    corpus+=  '\n----------------------------------------------------------------------'+\
                '---------------------------------------' 
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
        
        try:
            obra = sql.get_obra(self.combo.get().split(".")[0])
            self.lbljaja["text"]= self.combo.get() + '\n'+\
                'Ciudad: ' + obra[2] + '\nDirección: ' + obra[3] +\
                    '\nSaldo: $' + str(estado[0]-estado[1])
        except:
            pass
        
        fig = plt.figure(figsize=(3.3,1.9))
        #fig = Figure()
        
        objects = ('Ingresos','Gasto','Presupuesto')
        
        y_pos = np.arange(len(objects))
        
        plt.bar(y_pos, estado, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel('$')
        plt.title('Estado de la Obra')
        self.labeljiji = FigureCanvasTkAgg(fig, master=self.window)  # A tk.DrawingArea.
        self.labeljiji.draw()
        self.labeljiji.get_tk_widget().grid(column=0, row=1, sticky =(S))
        #self.labeljiji.get_tk_widget().destroy()
        plt.close('all')
    
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
            
    def agregar_obr(self,nm,ct,dr,ie,fim,fid,fia,fcm,fcd,fca,cerlib,lic,aptos,info):
        yd = {'ENE':1,'FEB':2,'MAR':3,'ABR':4,'MAY':5,'JUN':6,
             'JUL':7,'AGO':8,'SEP':9,'OCT':10,'NOV':11,'DIC':12}
        ini = main.validar_fecha(yd[fim],int(fid),int(fia))
        cul = main.validar_fecha(yd[fcm],int(fcd),int(fca))
        fat = False
        try:
            float(aptos)
        except:
            messagebox.showerror('Error', 'Ingrese un número de apartamentos válido')
            return False
        
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
        fi = str(fid) + '/' + str(yd[fim]) + "/" + str(fia)
        fc = str(fcd) + '/' + str(yd[fcm]) + "/" + str(fca)
        try:
            helper = sql.create_obra((nm,ct,dr,ie,fi,fc,cerlib,lic,aptos,info))
            self.rubros_por_defecto(helper)
            messagebox.showinfo('Crear Obra','Obra creada con éxito')

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
        
        sql.create_rubro((helper,"Expensas","Antes",0))
        sql.create_rubro((helper,"Permiso Planos","Antes",0))
        sql.create_rubro((helper,"Delimitación Urbana","Antes",0))
        sql.create_rubro((helper,"Distribución Planos","Antes",0))
        sql.create_rubro((helper,"Pre-Construcción","Antes",0))
        
        sql.create_rubro((helper,"Nomina Obreros","Durante",0))
        sql.create_rubro((helper,"Limpieza Lote - Personal","Durante",0))
        sql.create_rubro((helper,"Limpieza Lote - Volquetas","Durante",0))
        sql.create_rubro((helper,"Limpieza Lote - Retroexcavadora","Durante",0))
        sql.create_rubro((helper,"Pilotaje","Durante",0))
        sql.create_rubro((helper,"Placa Cimentación - Hierro","Durante",0))
        sql.create_rubro((helper,"Placa Cimentación - Casetón","Durante",0))
        sql.create_rubro((helper,"Placa Cimentación - Concretera","Durante",0))
        sql.create_rubro((helper,"Altura Obra - Cementera","Durante",0))
        sql.create_rubro((helper,"Altura Obra - Hierro","Durante",0))
        sql.create_rubro((helper,"Altura Obra - Montaje","Durante",0))
        sql.create_rubro((helper,"Agua","Durante",0))
        sql.create_rubro((helper,"Luz","Durante",0))
        sql.create_rubro((helper,"Gas","Durante",0))
        sql.create_rubro((helper,"Acabados - Cerámica","Durante",0))
        sql.create_rubro((helper,"Acabados - Electrodomésticos","Durante",0))
        sql.create_rubro((helper,"Acabados - Ornamentación","Durante",0))
        sql.create_rubro((helper,"Acabados - Pisos y Laminados","Durante",0))
        sql.create_rubro((helper,"Acabados - Drywall","Durante",0))
        sql.create_rubro((helper,"Acabados - Ascensor","Durante",0))
        sql.create_rubro((helper,"Acabados - Carpintería","Durante",0))
        sql.create_rubro((helper,"Acabados - Grifería","Durante",0))
               
        sql.create_rubro((helper,"Retorno Inversionistas","Después",0))
        sql.create_rubro((helper,"Escritura","Después",0))
        sql.create_rubro((helper,"Desenglobe","Después",0))
        sql.create_rubro((helper,"Permisos Ventas","Después",0))
        sql.create_rubro((helper,"Permiso IDU","Después",0))
        sql.create_rubro((helper,"Reglamento Propiedad Horizontal","Después",0))
              
        
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

    
    def agregar_transac(self,nombre,valor,cli):
        
        hue = sql.select_transacciones_obra(self.actual_obra)
        
        verify = nombre.split(": ")[0]
        realname = nombre.split(": ")[1]
        
        asociador = sql.get_rubro_by_nombre_obra((realname,self.actual_obra))
        
        if cli != "Ninguno":
            elkli = cli.split(' - ')[0]
        else:
            elkli = None
        
        if verify == "Entrada":
            sql.create_transaccion((self.actual_obra,
                                    self.actual_user,
                                    asociador,
                                    valor,
                                    'Entrada',
                                    elkli
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
                                    'Salida',
                                    elkli
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
                elvalor = valor.strip()
                if elvalor == '':
                    elvalor = 0
                valor = float(elvalor)
            except:
                messagebox.showerror('Error', 'Ingrese un valor numérico para el número de apartamentos')
                return False
        sql.update_obra((translate[nombre],valor,self.actual_obra))
        self.cargar_obras()
        self.actualizar_valores()
        messagebox.showinfo('Presupuesto','La información de la obra se actualizó con éxito')
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
            elif trial[theusr][0] != pw.get():
                messagebox.showerror('Error', 'Contraseña inválida')
            else:
                self.actual_user = theusr
                self.sudo = bool(trial[theusr][1])
                main.activar_todo(self) 
            self.master.destroy()
            if datetime.date.today().weekday() == 1:
                self.mostrar_facturas_pendientes(Toplevel(self.window))

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
                           "   Egresos: $"+str(data[0][1])+"   Utilidades: $" +
                           str(data[0][0]-data[0][1])
                           ,font=("Arial",10)) 
        
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
        self.master.geometry("370x440")
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
            self.lblv = Label(self.frame,text = "Información Adicional",font=("Arial",12))
            self.lblw = scrolledtext.ScrolledText(self.frame,width=40,height=7)
            self.lblw.insert(INSERT,data[10])
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
            self.lblest.pack()
            self.lblv.pack()
            self.lblw.pack()
            self.quit.pack()
            self.master.resizable(False, False)
            self.frame.pack()    
        
    #Ventana para Agregar Usuario
    def ventana_nuevo_usuario(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("280x250")
        self.frame = Frame(self.master)
         
        def close_window(self):
            self.master.destroy()
        
        def agregar_el_user(usr,pw,pw2,nm,su):
            trial = sql.select_all_users()
            theusr = usr.get().lower()
            if theusr in trial.keys():
                messagebox.showerror('Error', 'El usuario ya existe')
            elif pw2.get()!= pw.get():
                messagebox.showerror('Error', 'Las contraseñas deben coincidir')
            elif pw.get() == '':
                messagebox.showerror('Error', 'Las contraseña no debe ser vacía')
            else:
                if su.get() == 'Administrador':
                    sud = 1
                else: 
                    sud = 0
                sql.create_user((theusr,pw.get(),nm.get(),sud))
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
        self.lblsudo = Label(self.frame,text="Tipo de Usuario",font=("Arial",10))
        self.combse1 = Combobox(self.frame,width=32)
        if self.sudo:
            self.combse1['values'] = ('Normal','Administrador')
        else:
            self.combse1['values'] = ('Normal')
        self.combse1.current(0)
        self.agregar = Button(self.frame, text = "Registrar", 
                              command = lambda: agregar_el_user(self.entrus,
                                                                self.entrpw,
                                                                self.entrpw2,
                                                                self.entrnm,
                                                                self.combse1))
        self.lblus.pack()
        self.entrus.pack()
        self.lblnm.pack()
        self.entrnm.pack()
        self.lblpw.pack()
        self.entrpw.pack()
        self.lblpw2.pack()
        self.entrpw2.pack()
        self.lblsudo.pack()
        self.combse1.pack()
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
        def actualizar(cc):
            elid = cc.get().split(' - ')[0]
            jijiji = sql.select_transacciones_cliente((elid,))
            for i in self.transacs.get_children():
                self.transacs.delete(i)
            for i in jijiji:
                self.transacs.insert("",END,text=sql.get_obra(i[1])[1],
                                     values= (sql.get_nombre_rubro((i[3],)), i[4]))
            
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        self.transacs = Treeview(self.frame, columns = ("td", "id"))
        self.transacs.heading("#0", text="Obra")
        self.transacs.heading("td", text="Transaccion")
        self.transacs.heading("id", text="Valor")
        
        self.vsb = Scrollbar(self.frame, orient="vertical", command=self.transacs.yview)
        self.vsb.pack(side='right', fill='y')
        self.transacs.configure(yscrollcommand=self.vsb.set)
        
        cl = sql.select_all_clientes()
        listc = []
        for i in cl:
            listc.append(i[2]+" - "+i[0])
        listc = tuple(listc)
        
        self.comboclients = Combobox(self.frame,width=32)
        self.comboclients['values'] = listc
        self.actu = Button(self.frame, text = " Actualizar ", 
                           command = lambda : actualizar(self.comboclients))
        self.comboclients.pack()
        self.actu.pack()
        self.transacs.pack()
        self.quit.pack()
        self.master.resizable(False, False)
        self.frame.pack()        
    
        
    
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
            self.menus.entryconfig("Pagar Cuentas",state='disabled')
            self.menus.entryconfig("Ver Cobros Semana",state='disabled')
            self.cascada.entryconfig('Agregar Cliente',state='disabled')
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
            self.labeljiji.get_tk_widget().destroy()
            if self.master != None:
                self.master.destroy()
            
            
    #Ventana para Agregar Obra
    
    def ventana_agregar_o(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x465")
        self.frame = Frame(self.master)
          
        def close_window(self):
            self.master.destroy()
        
        def agregar_la_obra(self,nm,ct,dr,ie,fim,fid,fia,fcm,fcd,fca,crlib,licon,aptos,info):
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
                             aptos.get(),
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
        self.lblap = Label(self.frame,text="Apartamentos Disponibles",font=("Arial",10))
        self.entrap = Entry(self.frame,width=35)
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
                                                                self.entrap,
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
        self.lblap.grid(column=0,row=16)
        self.entrap.grid(column=0,row=17)         
        self.lbli.grid(column=0,row=18)
        self.entri.grid(column=0,row=19)
        self.blank.grid(column=0,row=20)
        self.quit.grid(column=0,row=21, sticky = (W))
        self.agregar.grid(column=0,row=21, sticky = (E))
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
                return
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
        self.master.geometry("250x200")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()      
        
        def agregar_trans(self,nombre,valor,cli):
            try:
                elvalor = valor.get().strip()
                if elvalor == '':
                    elvalor = 0
                float(elvalor)
                main.agregar_transac(self,
                                 nombre.get(),
                                 float(elvalor),
                                 cli.get())
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
            self.iclient = Combobox(self.frame,width=32)
            losclientes = sql.select_all_clientes()
            listc = ["Ninguno"]
            for i in losclientes:
                listc.append(i[2]+" - "+i[0])
            listc = tuple(listc)
        
            self.iclient['values'] = listc
            self.iclient.current(0)
            self.cbb.current(0)
            self.lblu = Label(self.frame,text="Ingrese Nueva Transacción",font=("Arial",10))
            self.lblcl = Label(self.frame,text="Seleccione cliente asociado",font=("Arial",10))
            self.entru = Entry(self.frame,width=35)
            self.agregar = Button(self.frame, text = "Agregar", 
                              command = lambda: agregar_trans(self,
                                                              self.cbb,
                                                              self.entru,
                                                              self.iclient))
            self.blank = Label(self.frame,text=" ")
            self.lbly.pack()
            self.cbb.pack()
            self.lblcl.pack()
            self.iclient.pack()
            self.lblu.pack()
            self.entru.pack()
            self.blank.pack()
            self.quit.pack(side = "left")
            self.agregar.pack(side = "right")
            self.master.resizable(False, False)
            self.frame.pack()

    #Ventana para Crear Contrato
    def ventana_agregar_cont(self,master):
         
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("250x370")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()
            self.quotes = []
        
        def cuota(self,cli):
            self.ventana_cuota(Toplevel(self.master),cli.get())
            
        def agregar_cont(self,apto,cli,tipocont):
            
            holii = self.agregar_contrato(apto.get(),cli.get(),tipocont.get())
            if holii:
                self.master.destroy()
                self.quotes = []
                self.actualizar_valores()

        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        
        if self.actual_obra == '':
            self.lblerr = Label(self.frame,text="No hay obras \n disponibles",font=("Arial",14))
            self.lblerr.pack()
            self.quit.pack()
            self.master.resizable(False, False)
            self.frame.pack()  
        
        else:
        
            self.lbly = Label(self.frame,text="Seleccionar Tipo Contrato",font=("Arial",10))
            self.cbb = Combobox(self.frame,width=32)
            self.cbb['values'] = ("Inversión","Venta","Préstamo")
            self.iclient = Combobox(self.frame,width=32)
            losclientes = sql.select_all_clientes()
            listc = []
            for i in losclientes:
                listc.append(i[0]+" ["+i[2]+"]")
            listc = tuple(listc)
        
            self.iclient['values'] = listc
            try:
                self.iclient.current(0)
            except:
                pass
            self.cbb.current(0)
            self.lblcl = Label(self.frame,text="Seleccione cliente asociado",font=("Arial",10))
            self.agregar = Button(self.frame, text = "Agregar Cuota", 
                              command = lambda: cuota(self,self.iclient))
            self.proceder = Button(self.frame, text = "Continuar", 
                              command = lambda: agregar_cont(self,
                                                              self.entrna,
                                                              self.iclient,
                                                              self.cbb
                                                              ))
            if len(listc) == 0:
                self.proceder.state(['disabled'])
                self.agregar.state(['disabled'])
                
            self.lblna = Label(self.frame,text="Ingrese Número Apartamento",font=("Arial",10))
            self.entrna = Entry(self.frame,width=35)
            
            self.cuotat = Label(self.frame,text="Cuotas actuales",font=("Arial",10))
            self.cuoticas = scrolledtext.ScrolledText(self.frame,width=27,height=10)
                
            self.blank = Label(self.frame,text=" ")
            self.lbly.pack()
            self.cbb.pack()
            self.lblcl.pack()
            self.iclient.pack()
            self.lblna.pack()
            self.entrna.pack()
            self.cuotat.pack()
            self.cuoticas.pack()            
            self.blank.pack()
            self.quit.pack(side = "left")
            self.proceder.pack(side = "right")
            self.agregar.pack(side = "right")
            self.master.resizable(False, False)
            self.frame.pack()

    def ventana_cuota(self,master,cliente):
         
        if self.minaster != None:
            self.minaster.destroy()

        self.minaster = master
        self.minaster.geometry("250x260")
        self.frame1 = Frame(self.minaster)
        
        def close_window(self):
            self.minaster.destroy()
            self.quotes = []

         
        def aggcuota(self,detalle,precio,dia,mes,anio,tipoc,estadop):
            sepudo = main.agregar_quo(self,detalle.get(),
                             precio.get(),
                             dia.get(),
                             mes.get(),
                             anio.get(),
                             tipoc.get(),
                             estadop.get())
            if sepudo:
                self.minaster.destroy()
                
                
        self.quit1 = Button(self.frame1, text = " Salir ", 
                           command = lambda : close_window(self))
            
        
        self.lbld = Label(self.frame1,text="Ingrese Valor",font=("Arial",10))
        self.entrd = Entry(self.frame1,width=35)
        
        self.lble = Label(self.frame1,text="Fecha Pago/Cobro",font=("Arial",10))
        self.combe1 = Combobox(self.frame1,width=8)        
        self.combe1['values'] = ('ENE','FEB','MAR','ABR','MAY','JUN',
                                 'JUL','AGO','SEP','OCT','NOV','DIC')
        self.combe1.current(0)
        self.combe2 = Combobox(self.frame1,width=8)
        self.combe2['values'] = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
                                 16,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
        self.combe2.current(0)
        self.combe3 = Combobox(self.frame1,width=8)
        self.combe3['values'] = (2015,2016,2017,2018,2019,2020,2021,2022,2023,
                                  2024,2025,2026,2027,2028,2029,2030,2031,2032,
                                  2033,2034,2035)
        self.combe3.current(0)
        
        self.lbld = Label(self.frame1,text="Concepto",font=("Arial",10))
        self.entrd = Entry(self.frame1,width=35)
        
        self.lblp = Label(self.frame1,text="Valor",font=("Arial",10))
        self.entrp = Entry(self.frame1,width=35)
        
        self.lble5 = Label(self.frame1,text="Estado de Pago",font=("Arial",10))
        self.combe5 = Combobox(self.frame1,width=32)
        self.combe5['values'] = ('Pagado','Por Pagar')
        self.combe5.current(0)
        
        self.lble4 = Label(self.frame1,text="Tipo de Cuota",font=("Arial",10))
        self.combe4 = Combobox(self.frame1,width=32)   
        self.combe4['values'] = ('Pago a Cliente','Cobro a Cliente')
        self.combe4.current(0)
        
        self.blank = Label(self.frame1,text=" ",font=("Arial",10))
        
        self.agregar1 = Button(self.frame1, text = "Agregar", 
                              command = lambda: aggcuota(self,
                                                              self.entrd,
                                                              self.entrp,
                                                              self.combe1,
                                                              self.combe2,
                                                              self.combe3,
                                                              self.combe4,
                                                              self.combe5))
        self.lbld.grid(column=0, row=0)
        self.entrd.grid(column=0, row=1)
        self.lblp.grid(column=0, row=2)
        self.entrp.grid(column=0, row=3)        
        self.lble4.grid(column=0, row=4)
        self.combe4.grid(column=0, row=5)
        self.lble5.grid(column=0, row=6)
        self.combe5.grid(column=0, row=7)
        self.lble.grid(column=0, row=8)
        self.combe1.grid(column=0, row=9,sticky = (W))
        self.combe2.grid(column=0, row=9,sticky = (N))
        self.combe3.grid(column=0, row=9,sticky = (E))
        self.blank.grid(column=0, row=10)
        self.quit1.grid(column=0, row=11,sticky = (W))
        self.agregar1.grid(column=0, row=11,sticky = (E))
        self.minaster.resizable(False, False)
        self.frame1.pack()
              
    def agregar_quo(self,detalle,precio,mes,dia,anio,tipoc,estadop):
        yd = {'ENE':1,'FEB':2,'MAR':3,'ABR':4,'MAY':5,'JUN':6,
             'JUL':7,'AGO':8,'SEP':9,'OCT':10,'NOV':11,'DIC':12}
        vad = main.validar_fecha(yd[mes],int(dia),int(anio))
        try:
            float(precio)
        except:
            messagebox.showerror('Error', 'Ingrese un valor de cuota válido')
            return False
        
        if not vad:
            messagebox.showerror('Error', 'La fecha no es válida')
            return False

        if detalle.strip() == '' :
            messagebox.showerror('Error', 'La cuota no puede registrarse con detalle vacío')
            return False
        fec = str(dia) + '/' + str(yd[mes]) + "/" + str(anio)
        if 1:
            self.quotes.append([0,0,0,float(precio),detalle,fec,tipoc,estadop])
            messagebox.showinfo('Crear Cuota','Cuota creada con éxito')
            self.actualizar_cuotas()

        else:
            messagebox.showerror('Error','La Cuota no pudo ser creada')
            return False
        self.actualizar_cuotas()
        return True

    def actualizar_cuotas(self):
        texto = ''
        for i in self.quotes:
            texto += str(i[4])+'\n'
            texto += str(i[3])+'\n'
            texto += i[7] + ' / '+ i[5]+'\n'
        
        self.cuoticas.delete(1.0,END)
        self.cuoticas.insert(INSERT,texto)
    
    #self.quotes.append([0,0,0,float(precio),detalle,fec,tipoc,estadop])
        
    def numero_aptos(self):
        return sql.get_aptos_obra((self.actual_obra,))
    
    def agregar_contrato(self,apto,cli,tipocont):
        if tipocont == 'Venta' and apto.strip()=='':
            messagebox.showerror('Error', 'No es posible realizar una venta sin un apartamento.')
            return False
        if self.numero_aptos() == 0:
            messagebox.showerror('Error', 'No hay apartamentos disponibles en esta obra')
            return False
        else:
            if 1:
                cli1 = cli.split('[')[1]
                cli1 = cli1.split(']')[0]
                fechita = datetime.date.today().strftime("%d/%m/%Y")
                helper = sql.create_contrato((self.actual_obra,
                                     self.actual_user,
                                     cli1,
                                     0,
                                     0,0,
                                     apto,
                                     tipocont,
                                     fechita))
                for i in self.quotes:
                    idcuotcre = sql.create_cuota((self.actual_obra,
                                     helper,
                                     cli1,
                                     i[3],
                                     i[4],
                                     i[5],
                                     i[6],
                                     i[7]))
                    if i[7] == 'Pagado':
                        j = sql.get_cuota(idcuotcre)
                        self.generar_factura(idcuotcre,cli1,j)
                sql.actualizar_saldo((helper,))
                if tipocont == 'Venta':
                    sql.descontar_apto((self.actual_obra,))
                messagebox.showinfo('Crear contrato','Contrato creado con éxito')
                return True
            else:
                messagebox.showerror('Error', 'No se pudo crear el contrato')
                return False
    
    def generar_factura(self,idcout,client,lacuot):
        
        pc = ''
        ingeg = ''
        ques = sql.get_tipocontrato_by_cuota((idcout,))
        print(ques)
        if ques == 'Venta':
            pc = 'Ventas'
            ingeg = 'Entrada'
        elif ques == 'Inversión':
            if lacuot[7] == 'Cobro a Cliente':
                pc = 'Inversionistas'
                ingeg = 'Entrada'
            elif lacuot[7] == 'Pago a Cliente':
                pc = 'Retorno Inversionistas'
                ingeg = 'Salida'
        elif ques == 'Préstamo':
            if lacuot[7] == 'Cobro a Cliente':
                pc = 'Préstamos'
                ingeg = 'Entrada'
            elif lacuot[7] == 'Pago a Cliente':
                pc = 'Retorno Inversionistas'
                ingeg = 'Salida'
        print(lacuot)       
        print(pc)
        idrub = sql.get_rubro_by_nombre_obra((pc,lacuot[1]))
        
        sql.create_transaccion((lacuot[1],
                                self.actual_user,
                                idrub,
                                lacuot[4],
                                ingeg,
                                client
                                ))
        sql.cambiar_pagado((idcout,))      
    
    
    def ventana_pagar_cuentas(self,master):
        
        if self.master != None:
            self.master.destroy()
        
        self.master = master
        self.master.geometry("450x100")
        self.frame = Frame(self.master)
        
        def close_window(self):
            self.master.destroy()      
        
        def pagarlo(self):
            num = int(self.cbct.get().split(" - ")[0])
            num = self.guidcuota[num]
            self.generar_factura(self.sinpagar[num][0],
                                 self.sinpagar[num][3],
                                 self.sinpagar[num])
            messagebox.showinfo('Pagar Cuenta','Cuenta Pagada')
            self.master.destroy()
            self.actualizar_valores()
            
  
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        self.pagar = Button(self.frame, text = "Pagar", 
                           command = lambda : pagarlo(self))
        
        self.cbct = Combobox(self.frame,width=67)
        self.sinpagar = sql.get_cuotas_por_pagar()
        print(self.sinpagar)
        self.valuespagar = []
        self.guidcuota = {}
        j = 0
        for i in self.sinpagar:
            self.guidcuota[i[0]] = j
            cl = sql.get_cliente(i[3])
            nomc = str(cl[0])+' ('+str(cl[2])+')'
            self.valuespagar.append(str(i[0]) + " - "+\
                               str(nomc)+ " - "+\
                               str(i[5])+ " - "+\
                               str(i[6])+ " - "+\
                               str(i[4]))
            j+=1
        self.cbct['values'] = tuple(self.valuespagar)
        if len(self.valuespagar) == 0:
            self.pagar.state(['disabled'])
        else:
            self.cbct.current(0)
        self.tit = Label(self.frame,text="Seleccione cuota a pagar",font=("Arial",10))
        self.tit.pack()
        self.cbct.pack()
        self.blank = Label(self.frame,text=" ",font=("Arial",10))
        self.blank.pack()
        self.quit.pack(side = "left")
        self.pagar.pack(side = "right")
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
            self.cbb['values'] = ('Nombre','Ciudad','Dirección',
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
        
    #Ventana para ver Historial Transacciones
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
                                   
    def mostrar_facturas_pendientes(self,master):
        if self.master != None:
            self.master.destroy()
        self.master = master
        self.frame = Frame(self.master)
        self.master.geometry("1030x260")
        self.frame = Frame(self.master)
                  
        def close_window(self):
            self.master.destroy()      
        
        self.quit = Button(self.frame, text = " Salir ", 
                           command = lambda : close_window(self))
        self.vista = Treeview(self.frame, columns = ("detalle", "tipo","valor","Fecha"))
        self.vsb = Scrollbar(self.frame, orient="vertical", command=self.vista.yview)
        self.vsb.pack(side='right', fill='y')
        self.vista.configure(yscrollcommand=self.vsb.set)
        
        self.vista.heading("#0", text="Cliente")
        self.vista.heading("detalle", text="Concepto")
        self.vista.heading("tipo", text="Tipo Cuota")
        self.vista.heading("valor", text="Valor")
        self.vista.heading("Fecha", text="Fecha")
        
        if self.actual_obra == '': 
            tr = []
        else:
            tr = sql.get_facturas_vencidas()
        for i in tr:

            datetime.date.today()
            nombre = sql.get_cliente(i[3])
            nombre = nombre[0] + ' - ' +nombre[1]

            self.vista.insert("",END,text=nombre,values=(i[5],
                              i[7],
                              i[4],
                              i[6]))
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
        
        self.labelji = ''
        
        
        def graph_1():
            
            if self.labelji != '':
                self.labelji.get_tk_widget().destroy()
            self.combograph['state']='disabled'
            
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
            self.labelji.get_tk_widget().pack(side="bottom")
            plt.close('all')
            
        def graph_2():
            
            if self.labelji != '':
                self.labelji.get_tk_widget().destroy()
            self.combograph['state']='disabled'
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

            plt.xlabel('Etapa del Proyecto')
            plt.ylabel('Dinero')
            plt.title('Presupuesto vs Gastos')
            plt.xticks(index + bar_width, ('Antes', 'Durante', 'Después'))
            plt.legend()
            
            plt.tight_layout()
            
            self.labelji = FigureCanvasTkAgg(fig, master=self.master)  # A tk.DrawingArea.
            self.labelji.draw()
            self.labelji.get_tk_widget().pack(side="bottom")
            plt.close('all')
            
        def graph_3():
            if self.labelji != '':
                self.labelji.get_tk_widget().destroy()
            self.combograph['state']='disabled'
            fig = plt.figure(figsize=(6,5))
            plt.clf()
            
            tag = ("Utilidad",)
            y_pos = np.arange(len(tag))
            
            
            entrada = 0
            gasto = 0
            
            for tran in trans:
                if tran[5]=="Entrada":
                    entrada+=tran[4]
                elif tran[5]=="Salida":
                    gasto+=tran[4]
            
            width = 0.5

            indices = np.arange(len(tag))

            plt.barh(tag, entrada, width, 
                     color='b', label='Ingreso')
            plt.barh(tag, gasto, 
                     width, color='r', label='Gasto')
            plt.title('La utilidad de esta obra es $' + str(entrada-gasto))

            plt.legend()
            
            self.labelji = FigureCanvasTkAgg(fig, master=self.master)  # A tk.DrawingArea.
            self.labelji.draw()
            self.labelji.get_tk_widget().pack(side="bottom")
            plt.close('all')
        
        def graph_4():
            if self.labelji != '':
                self.labelji.get_tk_widget().destroy()
            self.combograph['state']='readonly'
            
                        
            fig = plt.figure(figsize=(6,5))
            plt.clf()
            
            
            elrubroo = self.combograph.get()
            elrubro = 0
            presup = 0
            for i in rubs:
                if i[2] == elrubroo:
                    elrubro = i[0]
                    presup = i[4]
                    break
            gasto = 0

            for tran in trans:
                if tran[3]==elrubro:
                    gasto+=tran[4]
            
            n_groups = 1
            presupuestos = (presup)
            gastos = (gasto)

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

            plt.xlabel('Rubro')
            plt.ylabel('Dinero')
            plt.title(elrubroo)
            plt.xticks(index + bar_width, (' '))
            plt.legend()

            self.labelji = FigureCanvasTkAgg(fig, master=self.master)  # A tk.DrawingArea.
            self.labelji.draw()
            self.labelji.get_tk_widget().pack(side="bottom")            
            plt.close('all')
            
        def _quit():
                    # stops mainloop
            plt.close('all')
            self.master.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


        self.buttoon = Button(self.frame, text="Salir", command=_quit)
        self.buttoon.pack(side="right")
        self.buttoon1 = Button(self.frame, text="Porcentaje\nIngresos", command=graph_1)
        self.buttoon1.pack(side="left")
        self.buttoon2 = Button(self.frame, text="Presupuesto\npor etapas", command=graph_2)
        self.buttoon2.pack(side="left")
        self.buttoon3 = Button(self.frame, text="Vista de\nUtilidades", command=graph_3)
        self.buttoon3.pack(side="left")
        self.buttoon4 = Button(self.frame, text="Buscar\nRubro", command=graph_4)
        self.buttoon4.pack(side="left")
        self.combograph = Combobox(self.frame,width=32,state='disabled')
        rublist = []
        rub1 = sql.get_rubros_obra(self.actual_obra)
        for k in rub1:
            rublist.append(k.split(': ')[1])
        self.combograph['values'] = tuple(rublist)
        self.combograph.current(0)
        self.combograph.pack(side="left")
        if self.actual_obra != '':
            graph_1()
        
        self.master.resizable(False, False)
        self.frame.pack()
   
    

root = Tk()
app = main(root)
root.mainloop()
