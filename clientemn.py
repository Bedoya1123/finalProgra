#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from bs4 import BeautifulSoup
from requests import get
import Pyro4
from Tkinter import *
import ttk
import Tkinter as tk
import tkMessageBox
from PIL import ImageTk
from functools import partial
import sys, string, urllib
from urllib2 import urlopen
import re
import MySQLdb
import json
import ast
from functools import partial

@Pyro4.expose
class usuario():
	def __init__(self, id, usuario):
		self.id = id
		self.usuario = usuario
	def __str__(self):
		return self.usuario
class Cliente(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.initUI()

    def initUI(self):

         b = tk.Button()
         image = ImageTk.PhotoImage(file="login.png")
         b.config(image=image, bd=0)
         b.image = image
         b.pack()

         login = Frame(bd=4, relief='ridge')
         login.pack()

         Label(login, text="E-mail:", width=10, height=2, font=('MS', 10, 'bold')).pack()
         email = Entry(login)
         email.pack()

         Label(login, text="Password:", width=10, height=2, font=('MS', 10, 'bold')).pack()
         clave = Entry(login, show="*")
         clave.pack()


         f0 = tk.LabelFrame(login, width=100, height=100, relief='flat', borderwidth=4)
         f0.pack(padx=5, pady=5, side='left')
         Button(f0, text="Login", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda: self.ingresar(email, clave)).pack()

         f1 = tk.LabelFrame(login, width=100, height=100, relief='flat', borderwidth=4)
         f1.pack(padx=5, pady=5, side='left')
         Button(f1, text="Registrarse", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=self.registrar_usuario).pack()


    def registrar_usuario(self):

        self.idusuario = StringVar(value=1)

        register = Toplevel()

        Label(register, text="Nombre Completo:").pack()
        self.nombre = Entry(register)
        self.nombre.pack()

        Label(register, text="Apellidos:").pack()
        self.apellido = Entry(register)
        self.apellido.pack()

        Label(register, text="Password:").pack()
        self.clave = Entry(register, show="*")
        self.clave.pack()

        Label(register, text="E-mail:").pack()
        self.email = Entry(register)
        self.email.pack()

        Label(register, text="Seleccione el tipo de  usuario").pack()
        self.cbotemporadas = ttk.Combobox(register, textvariable=self.idusuario, state="readonly")
        self.cbotemporadas.pack()
        self.cbotemporadas.bind("<<ComboboxSelected>>", self.usuario_tipo)
        self.valores = self._cargaFromObject(o_usuario, self.cbotemporadas, "usuario", "id", seleccionado, self.idusuario)


        Button(register, text="Crear", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2, command=self.usuario_tipo).pack()


    def _cargaFromObject(self, coleccion, objeto, campodesc, campoid, val2select, variable):
        misc, misv = [], []
        for vv in coleccion:
            misv.append(getattr(vv, campodesc))
            misc.append(getattr(vv, campoid))
            if getattr(vv, campoid) == val2select: variable.set(getattr(vv, campodesc))
        objeto["values"] = misv
        return dict(zip(misv, misc))  # Crea diccionario



    def ingresar(self, email, clave):

        mail = email.get()
        pasw = clave.get()

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")# conexion servidor

        tipo = ingreso.login_usuario(mail, pasw)
        id_us = ingreso.obtener_idus(mail, pasw)
        if (tipo==0):
            tkMessageBox.showerror(title="Ingresar", message="Usuario o contraseña incorrecta")
        if (tipo==1):
            self.master.destroy()
            self.usuario_cliente(id_us)
        if (tipo==2):
            self.master.destroy()
            self.usuario_admin()


    def usuario_tipo(self):

        grabar = 1
        val = self.idusuario.get()
        id = self.valores[val]

        nom = self.nombre.get()
        ape = self.apellido.get()
        cl = self.clave.get()
        em = self.email.get()
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        if em == '' or cl == '':

           grabar = 0

        if grabar == 1:
            result = ingreso.login_register(nom, ape, id, cl, em)

            if (result==0):
               tkMessageBox.showinfo(title="Info", message="Usuario creado con exito")

            else:
               tkMessageBox.showerror(title="Error", message="Error al crear usuario")
        else:
            tkMessageBox.showinfo(title="Info", message="Todos los campos son obligatorios")





    def usuario_cliente(self, id_us):

        ventana_cliente = Tk()

        a = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="comprar.png")
        a.config(image=image, command=lambda: self.comprar(id_us), bd=0)
        a.image = image
        a.pack()

        b = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="puntos.png")
        b.config(image=image, command=lambda : self.puntos(id_us), bd=0)
        b.image = image
        b.pack()

        c = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="factura.png")
        c.config(image=image, command=lambda: self.factura_ver(id_us), bd=0)
        c.image = image
        c.pack()

        d = tk.Button(ventana_cliente)
        image = ImageTk.PhotoImage(file="salir.png")
        d.config(image=image, command=ventana_cliente.destroy, bd=0)
        d.image = image
        d.pack()
    def usuario_admin(self):

        ventana_admin = Tk()

        a = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="alertas.png")
        a.config(image=image, bd=0)
        a.image = image
        a.pack()

        b = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="paquetes.png")
        b.config(image=image, command= self.paquetesm, bd=0)
        b.image = image
        b.pack()

        c = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="ventas.png")
        c.config(image=image, bd=0)
        c.image = image
        c.pack()

        d = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="usuario.png")
        d.config(image=image, bd=0)
        d.image = image
        d.pack()

        e = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="log.png")
        e.config(image=image, bd=0)
        e.image = image
        e.pack()

        f = tk.Button(ventana_admin)
        image = ImageTk.PhotoImage(file="salir.png")
        f.config(image=image, command=ventana_admin.destroy, bd=0)
        f.image = image
        f.pack()



    def comprar(self, id_us):

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        result = ingreso.minutos_listar()
        resultado = ingreso.detalle_factura(id_us)

        self.ventanacomprar = Tk()
        self.ventanacomprar.geometry("1200x450+400+400")

        vp = tk.LabelFrame(self.ventanacomprar, width=650, height=20, relief='groove', borderwidth=4)
        vp.grid(row=0, column=0, padx=10, pady=2)

        Total = Label(vp, text='TOTAL:', justify=LEFT, fg='black', font=('MS', 8, 'bold'))
        Total.grid(row=0, column=0, columnspan=1, rowspan=1)
        self.Precio = Label(vp, text='$0', fg='black', width=10, font=('MS', 25, 'bold'))
        self.Precio.grid(row=1, column=0, columnspan=1, rowspan=1)



        Reci = Label(vp, text='EFETIVO:', justify=LEFT, fg='black', font=('MS', 8, 'bold'))
        Reci.grid(row=0, column=1, columnspan=1, rowspan=1)

        self.Re = Entry(vp)
        self.Re.grid(row=1, column=1, columnspan=1, rowspan=1)

        Button(vp, text="Calcular", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2,
               command=lambda id_us=id_us: self.calcular_cambio(id_us)).grid(row=2, column=1,columnspan=1, rowspan=1)
        Button(vp, text="Facturar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2,
               command=lambda: self.facturar(id_us)).grid(row=2, column=2, columnspan=1, rowspan=1)

        Cambio = Label(vp, text='CAMBIO:', justify=LEFT, fg='black', font=('MS', 8, 'bold'))
        Cambio.grid(row=0, column=2, columnspan=1, rowspan=1)

        self.Precioc = Label(vp, text='$0', fg='black', width=10, font=('MS', 20, 'bold'))
        self.Precioc.grid(row=1, column=2, columnspan=1, rowspan=1)

        vt = tk.LabelFrame(self.ventanacomprar, width=450, height=50, relief='flat', borderwidth=4)
        vt.grid(row=0, column=1, padx=10, pady=2)

        Titulo  = Label(vt, text='Paquetes Disponibles', bg='DodgerBlue4', fg='white', width=34, font=('MS', 20, 'bold'))
        Titulo.grid(row=0, column=0, columnspan=1, rowspan=1)

        vl = tk.LabelFrame(self.ventanacomprar, width=550, height=100, relief='flat', borderwidth=4)
        vl.grid(row=1, column=1, padx=10, pady=2)

        Title = Label(vl, text='Código', bg='DodgerBlue4', fg='white', width=5, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vl, text='Descripción', bg='DodgerBlue4', fg='white', width=20,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vl, text='Precio', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vl, text='Existencias', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)
        Title4 = Label(vl, text='Acción', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title4.grid(row=0, column=4, columnspan=1, rowspan=1)

        try:
            i = 1

            contenido4=[]
            for registro in result:
                codigo = registro[0]
                descrip = registro[1]
                precio = registro[2]
                exist = registro[3]
                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, text="%d" % (codigo), bg='turquoise3', fg='white', width=5,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1)

                Contenido1 = Label(vl, text="%s" % (descrip), bg='turquoise3', fg='white', width=20,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1)

                Contenido2 = Label(vl, text="%s" % (precio), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1)

                Contenido3 = Label(vl, text="%s" % (exist), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1)

                contenido4.append(Button(vl, text="Comprar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda codigo=codigo: self.insertar_linea(codigo, id_us)).grid(row="%d" % (i), column=4, columnspan=1, rowspan=1))

                i = i + 1

        except:
            print ("Error")
        self.grid_detalle(id_us)

    def grid_detalle(self, id_us):
        self.calcular_total(id_us)
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor
        resultado = ingreso.detalle_factura(id_us)
        vfact = tk.LabelFrame(self.ventanacomprar, width=550, height=100, relief='flat', borderwidth=4)
        vfact.grid(row=1, column=0, padx=10, pady=2)

        Title = Label(vfact, text='Código', bg='DodgerBlue4', fg='white', width=5, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vfact, text='Descripción', bg='DodgerBlue4', fg='white', width=20,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vfact, text='Cantidad', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vfact, text='Precio', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)
        Title4 = Label(vfact, text='Subtotal', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title4.grid(row=0, column=4, columnspan=1, rowspan=1)

        try:
            i = 1

            for registro in resultado:
                codigo = registro[1]
                descrip = registro[2]
                cantidad = registro[3]
                precio = registro[4]
                subtotal = registro[5]
                # Imprimimos los resultados obtenidos

                Contenido = Label(vfact, text="%d" % (codigo), bg='turquoise3', fg='white', width=5,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1)

                Contenido1 = Label(vfact, text="%s" % (descrip), bg='turquoise3', fg='white', width=20,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1)

                Contenido2 = Label(vfact, text="%s" % (cantidad), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1)

                Contenido3 = Label(vfact, text="%s" % (precio), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1)

                Contenido4 = Label(vfact, text="%s" % (subtotal), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido4.grid(row="%d" % (i), column=4, columnspan=1, rowspan=1)

                i = i + 1


        except:
            print("Error")

    def puntos(self, id_us):

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        result = ingreso.minutos_listar()
        resultado = ingreso.detalle_factura(id_us)

        self.ventanacomprar = Tk()
        self.ventanacomprar.geometry("1200x450+400+400")

        vp = tk.LabelFrame(self.ventanacomprar, width=650, height=20, relief='groove', borderwidth=4)
        vp.grid(row=0, column=0, padx=10, pady=2)

        Total = Label(vp, text='TOTAL:', justify=LEFT, fg='black', font=('MS', 8, 'bold'))
        Total.grid(row=0, column=0, columnspan=1, rowspan=1)

        tpuntos = ingreso.obtenerp(id_us)

        self.Precio = Label(vp, text='$0 ', fg='black', width=10, font=('MS', 25, 'bold'))
        self.Precio.grid(row=1, column=0, columnspan=1, rowspan=1)

        Button(vp, text="Facturar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2,
               command=lambda: self.facturar(id_us)).grid(row=2, column=2, columnspan=1, rowspan=1)

        puntos = Label(vp, text='PUNTOS:', justify=LEFT, fg='black', font=('MS', 8, 'bold'))
        puntos.grid(row=0, column=2, columnspan=1, rowspan=1)

        self.Ppunto = Label(vp, text='$0', fg='black', width=10, font=('MS', 20, 'bold'))
        self.Ppunto.configure(text='%s' % tpuntos)
        self.Ppunto.grid(row=1, column=2, columnspan=1, rowspan=1)

        vt = tk.LabelFrame(self.ventanacomprar, width=450, height=50, relief='flat', borderwidth=4)
        vt.grid(row=0, column=1, padx=10, pady=2)

        Titulo  = Label(vt, text='Paquetes Disponibles', bg='DodgerBlue4', fg='white', width=34, font=('MS', 20, 'bold'))
        Titulo.grid(row=0, column=0, columnspan=1, rowspan=1)

        vl = tk.LabelFrame(self.ventanacomprar, width=550, height=100, relief='flat', borderwidth=4)
        vl.grid(row=1, column=1, padx=10, pady=2)

        Title = Label(vl, text='Código', bg='DodgerBlue4', fg='white', width=5, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vl, text='Descripción', bg='DodgerBlue4', fg='white', width=20,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vl, text='Puntos', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vl, text='Existencias', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)
        Title4 = Label(vl, text='Acción', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title4.grid(row=0, column=4, columnspan=1, rowspan=1)

        try:
            i = 1

            contenido4=[]
            for registro in result:
                codigo = registro[0]
                descrip = registro[1]
                puntos = registro[5]
                exist = registro[3]
                # Imprimimos los resultados obtenidos

                Contenido = Label(vl, text="%d" % (codigo), bg='turquoise3', fg='white', width=5,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1)

                Contenido1 = Label(vl, text="%s" % (descrip), bg='turquoise3', fg='white', width=20,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1)

                Contenido2 = Label(vl, text="%s" % (puntos), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1)

                Contenido3 = Label(vl, text="%s" % (exist), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1)

                contenido4.append(Button(vl, text="Canjear", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda codigo=codigo : self.insertar_lineap(codigo, id_us)).grid(row="%d" % (i), column=4, columnspan=1, rowspan=1))

                i = i + 1

        except:
            print ("Error")
        self.grid_detallepuntos(id_us)

    def grid_detallepuntos(self, id_us):
        self.calcular_total(id_us)
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor
        resultado = ingreso.detalle_factura(id_us)
        vfact = tk.LabelFrame(self.ventanacomprar, width=550, height=100, relief='flat', borderwidth=4)
        vfact.grid(row=1, column=0, padx=10, pady=2)

        Title = Label(vfact, text='Código', bg='DodgerBlue4', fg='white', width=5, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vfact, text='Descripción', bg='DodgerBlue4', fg='white', width=20,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vfact, text='Cantidad', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vfact, text='Puntos', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)
        Title4 = Label(vfact, text='Precio', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title4.grid(row=0, column=4, columnspan=1, rowspan=1)
        Title5 = Label(vfact, text='Subtotal', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title5.grid(row=0, column=5, columnspan=1, rowspan=1)

        try:
            i = 1

            for registro in resultado:
                codigo = registro[1]
                descrip = registro[2]
                cantidad = registro[3]
                precio = registro[4]
                subtotal = registro[5]
                puntos = registro[8]
                # Imprimimos los resultados obtenidos

                Contenido = Label(vfact, text="%d" % (codigo), bg='turquoise3', fg='white', width=5,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1)

                Contenido1 = Label(vfact, text="%s" % (descrip), bg='turquoise3', fg='white', width=20,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1)

                Contenido2 = Label(vfact, text="%s" % (cantidad), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1)

                Contenido3 = Label(vfact, text="%s" % (puntos), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1)

                Contenido4 = Label(vfact, text="%s" % (precio), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido4.grid(row="%d" % (i), column=4, columnspan=1, rowspan=1)

                Contenido5 = Label(vfact, text="%s" % (subtotal), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido5.grid(row="%d" % (i), column=5, columnspan=1, rowspan=1)

                i = i + 1


        except:
            print("Error")
    def facturar(self, id_us):
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor
        ingreso.guardar_factura(id_us)
        self.ventanacomprar.destroy()

    def insertar_linea(self, id_paqute, id_us):

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        ingreso.insertarlinea(id_paqute, id_us)
        self.grid_detalle(id_us)

    def insertar_lineap(self, id_paqute, id_us):

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        ingreso.insertarlinea(id_paqute, id_us)
        self.grid_detallepuntos(id_us)
    def calcular_total(self, id_us):
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor
        total = ingreso.totallineas(id_us)
        self.Precio.config(text='%s' % total)

    def calcular_cambio(self, id_us):

        efet = int(self.Re.get())

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor
        totalf = ingreso.totallineas(id_us)

        cambio = efet - totalf
        self.Precioc.config(text='%s' % cambio)



    def factura_ver(self, id_us):

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor
        result = ingreso.ver_factura(id_us)

        verf = Tk()

        vfact = tk.LabelFrame(verf, width=550, height=100, relief='flat', borderwidth=4)
        vfact.grid(row=0, column=0, padx=10, pady=2)

        Title = Label(vfact, text='fecha', bg='DodgerBlue4', fg='white', width=15, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vfact, text='Numero de Factura', bg='DodgerBlue4', fg='white', width=20,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vfact, text='Total Compra', bg='DodgerBlue4', fg='white', width=20,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vfact, text='Total Puntos', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)

        Title3 = Label(vfact, text='Acción', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=4, columnspan=1, rowspan=1)

        i = 1
        contenido4 = []
        for registro in result:
                nfactura = registro[0]
                fecha = registro[1]
                tcompra = registro[8]
                tpuntos = registro[9]
                # Imprimimos los resultados obtenidos

                Contenido = Label(vfact, text="%s" % (fecha), bg='turquoise3', fg='white', width=15,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1)

                Contenido1 = Label(vfact, text="%d" % (nfactura), bg='turquoise3', fg='white', width=20,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1)

                Contenido2 = Label(vfact, text="%d" % (tcompra), bg='turquoise3', fg='white', width=20,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1)

                Contenido3 = Label(vfact, text="%d" % (tpuntos), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1)

                contenido4.append(Button(vfact, text="Ver Factura", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
                                         activebackground="turquoise3", width=10, height=2,
                                         command=lambda nfactura=nfactura, id_us = id_us: self.verdetalle(nfactura, id_us)).grid(row="%d" % (i), column=4, columnspan=1, rowspan=1))

                i = i + 1
    def verdetalle(self, nfactura, id_us):

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor
        result = ingreso.ver_dfactura(nfactura, id_us)
        verdetalle = Tk()


        vdt = tk.LabelFrame(verdetalle, width=550, height=100, relief='flat', borderwidth=4)
        vdt.grid(row=0, column=0, padx=10, pady=2)

        Title = Label(vdt, text='Código', bg='DodgerBlue4', fg='white', width=15, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vdt, text='Producto', bg='DodgerBlue4', fg='white', width=20,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vdt, text='Cantidad', bg='DodgerBlue4', fg='white', width=20,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vdt, text='Precio', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)

        Title3 = Label(vdt, text='Subtotal', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=4, columnspan=1, rowspan=1)

        i = 1

        for registro in result:
            codigo = registro[1]
            nombre = registro[2]
            cantidad = registro[3]
            precio = registro[4]
            subtotal = registro[5]
            # Imprimimos los resultados obtenidos

            Contenido = Label(vdt, text="%s" % (codigo), bg='turquoise3', fg='white', width=15,
                              font=('MS', 10, 'bold'))
            Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1)

            Contenido1 = Label(vdt, text="%s" % (nombre), bg='turquoise3', fg='white', width=20,
                               font=('MS', 10, 'bold'))
            Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1)

            Contenido2 = Label(vdt, text="%d" % (cantidad), bg='turquoise3', fg='white', width=20,
                               font=('MS', 10, 'bold'))
            Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1)

            Contenido3 = Label(vdt, text="%d" % (precio), bg='turquoise3', fg='white', width=10,
                               font=('MS', 10, 'bold'))
            Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1)


            Contenido4 = Label(vdt, text="%d" % (subtotal), bg='turquoise3', fg='white', width=10,
                               font=('MS', 10, 'bold'))
            Contenido4.grid(row="%d" % (i), column=4, columnspan=1, rowspan=1)
            i = i + 1



    def paquetesm(self):

        self.ventanapaquetes = Tk()
        self.ventanapaquetes.geometry("1200x450+400+400")


        vpq = tk.LabelFrame(self.ventanapaquetes, width=450, height=50, relief='flat', borderwidth=4)
        vpq.grid(row=0, column=0, padx=10, pady=2)



        Label(vpq, text="Descripción:", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=0, columnspan=1, rowspan=1)
        nombre = Entry(vpq)
        nombre.grid(row=2, column=0, columnspan=1, rowspan=1)

        Label(vpq, text="Precio", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=1, columnspan=1, rowspan=1)
        precio = Entry(vpq)
        precio.grid(row=2, column=1, columnspan=1, rowspan=1)

        Label(vpq, text="Existencia", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=2, columnspan=1, rowspan=1)
        inventario = Entry(vpq)
        inventario.grid(row=2, column=2, columnspan=1, rowspan=1)

        Label(vpq, text="Stock", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, column=3, columnspan=1, rowspan=1)
        stock = Entry(vpq)
        stock.grid(row=2, column=3, columnspan=1, rowspan=1)

        Button(vpq, text="Crear", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2).grid(row=2, column=4, columnspan=1, rowspan=1)

        Button(vpq, text="Actualizar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2).grid(row=2, column=5, columnspan=1, rowspan=1)
        self.actventana()

    def actventana(self):
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        result = ingreso.minutos_listar()
        vp = tk.LabelFrame(self.ventanapaquetes, width=550, height=100, relief='flat', borderwidth=4)
        vp.grid(row=1, column=0, padx=5, pady=2)

        Title = Label(vp, text='Código', bg='DodgerBlue4', fg='white', width=5, font=('MS', 10, 'bold'))
        Title.grid(row=0, column=0, columnspan=1, rowspan=1)
        Title1 = Label(vp, text='Descripción', bg='DodgerBlue4', fg='white', width=20,
                       font=('MS', 10, 'bold'))
        Title1.grid(row=0, column=1, columnspan=1, rowspan=1)
        Title2 = Label(vp, text='Precio', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title2.grid(row=0, column=2, columnspan=1, rowspan=1)
        Title3 = Label(vp, text='Existencias', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title3.grid(row=0, column=3, columnspan=1, rowspan=1)

        Title4 = Label(vp, text='Stock Minimo', bg='DodgerBlue4', fg='white', width=10,
                       font=('MS', 10, 'bold'))
        Title4.grid(row=0, column=4, columnspan=1, rowspan=1)

        try:
            i = 1

            for registro in result:
                codigo = registro[0]
                descrip = registro[1]
                precio = registro[2]
                exist = registro[3]
                minimo = registro[4]
                # Imprimimos los resultados obtenidos

                Contenido = Label(vp, text="%d" % (codigo), bg='turquoise3', fg='white', width=5,
                                  font=('MS', 10, 'bold'))
                Contenido.grid(row="%d" % (i), column=0, columnspan=1, rowspan=1)

                Contenido1 = Label(vp, text="%s" % (descrip), bg='turquoise3', fg='white', width=20,
                                   font=('MS', 10, 'bold'))
                Contenido1.grid(row="%d" % (i), column=1, columnspan=1, rowspan=1)

                Contenido2 = Label(vp, text="%s" % (precio), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido2.grid(row="%d" % (i), column=2, columnspan=1, rowspan=1)

                Contenido3 = Label(vp, text="%s" % (exist), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido3.grid(row="%d" % (i), column=3, columnspan=1, rowspan=1)

                Contenido4 = Label(vp, text="%s" % (minimo), bg='turquoise3', fg='white', width=10,
                                   font=('MS', 10, 'bold'))
                Contenido4.grid(row="%d" % (i), column=4, columnspan=1, rowspan=1)

                i = i + 1

        except:
            print("Error")

    def veliminar(self):

        ventana_eliminar = Tk()

        Label(ventana_eliminar, text="Ingrese el nombre de la pagina a eliminar :").pack()
        eliminar = Entry(ventana_eliminar)
        eliminar.pack()

        Button(ventana_eliminar, text="Borrar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'), activebackground="turquoise3", width=10, height=2, command=lambda: self.eliminar_pag(eliminar)).pack()



    def eliminar_pag(self, eliminar):

        elim = eliminar.get()
        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        id = ingreso.pagina_eliminar(elim)

        if (id==0):
            tkMessageBox.showinfo(title="Info", message="la pagina se elimino con exito")

        else:
            tkMessageBox.showerror(title="Error", message="El registro no existe")


    def vinsertar(self):
        ventanaagregar = Tk()
        ventanaagregar.title("Agregar pagina web")

        ventanaagregar.geometry("340x140+500+550")

        Label(ventanaagregar, text="Nombre:", width=10, height=2, font=('MS', 10, 'bold')).grid(row=1, sticky=W)
        nombre = Entry(ventanaagregar)
        Label(ventanaagregar, text="Dominio:", width=10, height=2, font=('MS', 10, 'bold')).grid(row=2, sticky=W)
        dominio = Entry(ventanaagregar)
        nombre.grid(row=1, column=1)
        dominio.grid(row=2, column=1)

        Button(ventanaagregar, text="Crear", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2, command=lambda: self.insertar_pag(nombre, dominio)).grid(row=3, column=1)

    def insertar_pag(self, nombre, dominio):

        grabar = 1

        nom = nombre.get()
        url = dominio.get()

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor
        if nom == '' or url == '':

           grabar = 0

        if grabar == 1:
            result = ingreso.pagina_insertar(nom, url)

            if (result==0):
               tkMessageBox.showinfo(title="Info", message="Pagina creada con exito")

            else:
               tkMessageBox.showerror(title="Error", message="Error al crear la pagina")
        else:
            tkMessageBox.showinfo(title="Info", message="Todos los campos son obigatorios")


    def vseo(self):

        seo = Tk()

        Button(seo, text="Contar Palabras", bg="aquamarine", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2, command=self.contar_palabras).grid(row=1, column=1)
        Button(seo, text="Diccionario", bg="aquamarine1", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=1, column=2)
        Button(seo, text="Contar Imagenes", bg="aquamarine2", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2, command=self.contar_img).grid(row=1, column=3)

        Button(seo, text="Contar enlaces", bg="aquamarine3", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=1, column=4)
        Button(seo, text="Analizar Url", bg="aquamarine4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=1, column=5)
        Button(seo, text="Analizar Palabras claves", bg="azure", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=1)
        Button(seo, text="Redes sociales", bg="azure1", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=2)
        Button(seo, text="Estructura del sitio", bg="azure2", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=3)
        Button(seo, text="Contenido No Apto", bg="azure3", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=4)
        Button(seo, text="Contenido Dudoso", bg="azure4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=2, column=5)
        Button(seo, text="Malas practicas", bg="CadetBlue", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=3, column=1)
        Button(seo, text="Librerias Usadas", bg="CadetBlue1", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=3, column=2)
        Button(seo, text="Comprobar enlaces externos", bg="CadetBlue2", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=3, column=3)
        Button(seo, text="Más Puntuación", bg="CadetBlue3", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=20, height=2).grid(row=3, column=4)

    def contar_palabras(self):

        ventana_contar = Tk()

        Label(ventana_contar, text="Ingrese el ID  de la pagina:").pack()
        contar = Entry(ventana_contar)
        contar.pack()

        print (contar)
        Button(ventana_contar, text="Enviar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2, command=lambda: self.contarp(contar)).pack()

    def contarp(self, contar):
        con = contar.get()

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        result = ingreso.palabras_cont(con)

        print (result)

    def contar_img(self):

        ventana_img = Tk()

        Label(ventana_img, text="Ingrese el ID  de la pagina:").pack()
        contar = Entry(ventana_img)
        contar.pack()

        Button(ventana_img, text="Enviar", bg="turquoise4", bd=0, fg='white', font=('MS', 10, 'bold'),
               activebackground="turquoise3", width=10, height=2, command=lambda: self.contarimg(contar)).pack()

    def contarimg(self, contar):

        con = contar.get()

        ingreso = Pyro4.Proxy("PYRONAME:Leidy.Cristian")  # conexion servidor

        result = ingreso.contar_imagenes(con)

        print (result)

def creavalores():
	c = usuario(1,"Cliente")
	o_usuario.append(c)
	c = usuario(2,"Administrador")
	o_usuario.append(c)


o_usuario = []
seleccionado = 2
def main():
    creavalores()
    ventana = Tk()
    app = Cliente(ventana)
    ventana.geometry("400x480+300+300")
    ventana.mainloop()

if __name__ == '__main__':
    main()