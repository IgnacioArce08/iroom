#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import json
import urllib3
import mysql.connector

db = mysql.connector.connect(host = "localhost", user = "adroom", passwd = "adminroom", db = "iroom")

type_sensor = ['temperature', 'humidity', 'light', 'sound', 'motion']
last_value = [0,0,0,0,0,0,0,0]

#PONER LA IP DE LA MÁQUINA VIRTUAL EN LA QUE ESTÉ CORRIENDO EL EMULADOR
server = 'http://127.0.0.1:8000/'
#server = 'http://10.0.21.132:8000/'
http = urllib3.PoolManager()
def updateSensor(code):
	value = 0
	try:

		""" PARTE 1:COMPLETAR AQUÍ EL CÓDIGO PARA LLEER EL VALOR DE UN SENSOR CON API REST"""

	except ValueError:
		print ('Error de leer dato de sensor')
	if value != last_value[code]:
		try:

			""" PARTE 1: COMPLETAR AQUÍ EL CÓDIGO PARA ESCRIBIR EN LA BASE DE DATOS EL VALOR DEL SENSOR"""

		except ValueError:
			print ('Error al insertar en base de datos')

def controlLightColor():
	try:
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='red' order by time desc""")
		red = int(cursor.fetchone()[0])
		if (red != last_value[5]):
			last_value[5] = red
			print ("red:" + str(red))
			response = http.request('PUT', server+'red/'+str(red))
	except ValueError:
		print ('Error al consultar de base de datos o conectar con iroom')

		""" PARTE 1: COMPLETAR AQUI EL RESTO DE CÓDIGO PARA PROCESAR EL COLOR VERDE Y AZUL"""

if __name__ == "__main__":
	cursor=db.cursor(buffered=True)
	cursor.execute ("""DROP table sensors""")
	cursor.execute ("""create table sensors( time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, nombre VARCHAR(15), valor INTEGER)""")
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('temperature', 20))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('humidity', 40))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('light', 30))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('sound', 10))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('motion', 0))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('red', 20))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('blue', 20))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('green', 20))
	db.commit()
	print ('Base de datos creada, comienza la consulta de sensores')
	while True:
		for code in range(0, 5):
			updateSensor(code)
			time.sleep(1)
		controlLightColor()
