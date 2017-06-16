#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import Pyro4
from bs4 import BeautifulSoup
import bs4 as bs
from requests import get
import json
import MySQLdb
etiquetas_imagenes= list()
import re, string
import mysql.connector


@Pyro4.expose
class Servidor(object):

    @Pyro4.expose

    def conexionbd(self):
        HOST = 'localhost'
        USER = 'root'
        PASSWORD = ''
        DATABASE = 'minutos'
        conexion = (HOST, USER, PASSWORD, DATABASE)
        conn = MySQLdb.connect(*conexion)  # Conectar a la base de datos
        return conn

    @property
    def run_query(self, query):
        cursor = self.conexionbd()
        cursor.execute(query)  # Ejecutar una consulta
        if query.upper().startswith('SELECT'):
            data = self.cursor.fetchall()  # Traer los resultados de un select
        else:
            conn.commit()  # Hacer efectiva la escritura de datos
            data = None

        cursor.close()  # Cerrar el cursor
        conn.close()  # Cerrar la conexión
        return data


    @Pyro4.expose
    def login_usuario(self, email, clave):#login

        conexion= self.conexionbd()
        cursor = conexion.cursor()


        sql = "SELECT id_tipo FROM usuario WHERE email = '%s' AND clave = '%s'" % (email, clave)
        cursor.execute(sql)  # Ejecutar una consulta

        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0
        return datos
        print (datos)

    def obtener_idus(self, email, clave):# obtener id_usuario

        conexion= self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT id_usuario FROM usuario WHERE email = '%s' AND clave = '%s'" % (email, clave)
        cursor.execute(sql)  # Ejecutar una consulta
        result = cursor.fetchall()
        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0

        return datos


    def login_register(self, nombre, apellido, id, clave, email): #insertar registros de usuario

        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor

        sql = "INSERT INTO usuario (nombre, apellido, clave, id_tipo, email ) VALUES ('%s','%s','%s',%d,'%s')" % (nombre, apellido, clave, id, email)

        cursor.execute(sql)
        conexion.commit()
        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0

        return datos

    def obtener_cliente(self, id_us):
        conexion = self.conexionbd()
        cursor = conexion.cursor()

        sql = "SELECT cedula, nombre, apellido, telefono, direccion FROM usuario WHERE id_usuario = '%s'" % (id_us)

        print (sql)
        cursor.execute(sql)  # Ejecutar una consulta

        result = cursor.fetchall()

        return result

    def guardar_factura(self, id_us):
         # traes informacion del cliente para guardar la factura
        resultado = self.obtener_cliente(id_us)
        total = self.totallineas(id_us)

        tasacambio = 5000.00
        puntos = total / tasacambio
        for registro in resultado:
            vcedula = registro[0]
            nombre = registro[1]
            apellido = registro[2]
            telefono = registro[3]
            direccion = registro[4]
        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "INSERT INTO factura (fecha, id_usuario, cedula, nombre, apellido, telefono, direccion, total, puntos) VALUES (curdate(), %d, '%s','%s','%s','%s','%s', %d, %d)" % (id_us, vcedula, nombre, apellido, telefono, direccion, total, puntos)
        cursor.execute(sql)
        conexion.commit()
        #Actualizar punto del cliente
        sql = "UPDATE usuario SET puntos = puntos + %d  WHERE id_usuario = %d" % (puntos, id_us)
        cursor.execute(sql)
        conexion.commit()
        # Obtener el numero de la factura insertada
        sql = "SELECT MAX(id_factura) FROM factura"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for registro in resultado:
            nro = registro[0]
         # Actualizar detalle de la factura a estado de guardado y asociar a la factura
        sql = "UPDATE tmp_detalle SET grabado = 1, id_factura = %d  WHERE id_usuario = %d AND grabado = 0" % (nro, id_us)
        cursor.execute(sql)
        conexion.commit()
        self.actualizar_inv(nro)

    @Pyro4.expose
    def ver_factura(self, id_us):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM factura  WHERE id_usuario = %d" % (id_us)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados


    def ver_dfactura(self, nfactura, id_us):

        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM tmp_detalle  WHERE id_factura = %d  AND id_usuario = %d" % (nfactura, id_us)
        print(sql)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados

    def actualizar_inv(self, id_factura):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        print("paso")
        sql = "SELECT  id_paquete, cantidad  FROM tmp_detalle WHERE id_factura = %d" % (id_factura)
        print(sql)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        for registro in resultados:
            id_paquete = registro[0]
            cantidad = registro[1]
            self.actualizar_paq(cantidad, id_paquete)


    def actualizar_paq(self, cantidad, id_paquete): # actualizar pagina de paquetes de minutos
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "UPDATE paquete SET existencia = existencia - %d WHERE id_paquete = %d" % (cantidad, id_paquete)
        cursor.execute(sql)
        conexion.commit()


    def insertarlinea(self, id_paq, id_us): # agregar producto antes de facturar
        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        if self.buscarlinea(id_paq, id_us)==0:

            sql = "INSERT INTO tmp_detalle (id_usuario, id_paquete, nombre, cantidad, precio, subtotal, grabado, puntos) SELECT '%s', id_paquete, nombre, 1, precio, precio, 0, puntos FROM paquete where id_paquete = '%d'" % (id_us, id_paq)
            print(sql)

        else:
            puntos_paq = self.obtener_puntosp(id_paq)
            sql = "UPDATE tmp_detalle SET cantidad = cantidad + 1, subtotal = cantidad * precio, puntos = cantidad * %s WHERE id_paquete = %s AND id_usuario = %s AND grabado = 0" % (puntos_paq, id_paq, id_us)
            print(sql)
        cursor.execute(sql)
        conexion.commit()

    def obtener_puntosp(self, id_paq):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT puntos FROM paquete WHERE id_paquete = %d" % id_paq
        cursor.execute(sql)
        resultado = cursor.fetchall()
        for registro in resultado:
            puntos_paq = registro[0]
        return puntos_paq


    def buscarlinea(self, id_paq, id_us):
        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "SELECT * FROM tmp_detalle WHERE id_paquete = %s AND id_usuario = %s AND grabado = 0" % (id_paq, id_us)
        print(sql)
        cursor.execute(sql)
        resultado = cursor.fetchall()
        r = 0
        if resultado:
            r = 1
        print (r)
        return r

    def totallineas(self, id_us):# Calcular total factura
        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "SELECT SUM(subtotal) FROM tmp_detalle WHERE id_usuario = %d AND grabado = 0" % (id_us)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        for registro in resultados:
            total = registro[0]

        return total




    def minutos_listar(self):
        conexion=self.conexionbd()
        cursor=conexion.cursor()
        sql = "SELECT * FROM paquete"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados

    def detalle_factura(self, id_us):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT * FROM tmp_detalle WHERE id_usuario = %d AND grabado = 0" % (id_us)
        print (sql)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        return resultados

    @Pyro4.expose

    def obtenerp(self, id_us):
        conexion = self.conexionbd()
        cursor = conexion.cursor()
        sql = "SELECT puntos  FROM usuario WHERE id_usuario = %d" % (id_us)
        print(sql)
        cursor.execute(sql)
        resultados = cursor.fetchall()
        for registro in resultados:
            puntos = registro[0]

        return puntos

    def pagina_eliminar(self, pagina):


        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "DELETE FROM pagina WHERE id_pagina = %s" % (pagina)


        cursor.execute(sql)
        conexion.commit()
        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0

        return datos


    def pagina_insertar(self, nombre, url):

        conexion = self.conexionbd()
        cursor = conexion.cursor()  # Crear un cursor
        sql = "INSERT INTO pagina (nombre, url) VALUES ('%s','%s')" % (nombre, url)

        cursor.execute(sql)
        conexion.commit()
        result = cursor.fetchall()

        if result:
            for registro in result:
                datos = registro[0]

        else:
            datos = 0

        return datos




def main():
    demonio = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = demonio.register(Servidor)
    ns.register("Leidy.Cristian", uri)
    print ("estoy corriendo")
    demonio.requestLoop()

if __name__ == "__main__":
    main()
