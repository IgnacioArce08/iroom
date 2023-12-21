#!/usr/bin/python
# -- coding: utf-8 --

import os
import time
import json
import urllib3
import mysql.connector

db = mysql.connector.connect(host = "localhost", user = "nacho", passwd = "@Nacho08", db = "iroom")
cursor = db.cursor()

type_sensor = ['temperature', 'humidity', 'light', 'sound', 'motion']
last_value = [0,0,0,0,0,0,0,0]

#PONER LA IP DE LA MÁQUINA VIRTUAL EN LA QUE ESTÉ CORRIENDO EL EMULADOR
server = 'http://127.0.0.1:8000/'
server = 'http://192.168.56.103:8000/'
http = urllib3.PoolManager()
def updateSensor(code):
	
	value = 0
	try:
		""" PARTE 1:COMPLETAR AQUÍ EL CÓDIGO PARA LLEER EL VALOR DE UN SENSOR CON API REST"""
		response = http.request('GET', f'{server}{type_sensor[code]}')
		data = json.loads(response.data)
		value = data[type_sensor[code]]
		
	except ValueError:
		print ('Error de leer dato de sensor')
		
	if value != last_value[code]:
		try:

			""" PARTE 1: COMPLETAR AQUÍ EL CÓDIGO PARA ESCRIBIR EN LA BASE DE DATOS EL VALOR DEL SENSOR"""
			cursor.execute("""INSERT INTO sensors(nombre, valor) VALUES (%s, %s)""", (type_sensor[code], value))
			last_value[code] = value
			db.commit() 

		except ValueError:
			print ('Error al insertar en base de datos')
			db.rollback()

def controlLightColor():
	try:
		cursor.execute ("""SELECT valor FROM sensors WHERE nombre='red' order by time desc""")
		red = int(cursor.fetchone()[0])

		cursor.execute("""SELECT valor FROM sensors WHERE nombre='green' order by time desc""")
		green = int(cursor.fetchone()[0])

		cursor.execute("""SELECT valor FROM sensors WHERE nombre='blue' order by time desc""")
		blue = int(cursor.fetchone()[0])
		
		if (red != last_value[5] or green != last_value[6] or blue != last_value[7]):
			last_value[5] = red
			last_value[6] = green
			last_value[7] = blue
	
			response_red = http.request('PUT', 'http://192.168.44.131:8000/red/'+str(red))
			response_green = http.request('PUT', 'http://192.168.44.131:8000/green/'+str(green))
			response_blue = http.request('PUT', 'http://192.168.44.131:8000/blue/'+str(blue))
			
			print("Color RGB: Red - " + str(red) + "Green -" + str(green) + "Blue -" + str(blue))
	except ValueError:
		print ('Error al consultar de base de datos o conectar con iroom')

		""" PARTE 1: COMPLETAR AQUI EL RESTO DE CÓDIGO PARA PROCESAR EL COLOR VERDE Y AZUL"""

if _name_ == "_main_":
	cursor=db.cursor(buffered=True)
	cursor.execute ("""DROP table sensors""")
	cursor.execute ("""create table sensors( time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, nombre VARCHAR(15), valor INTEGER)""")
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('temperature', 20))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('humidity', 40))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('light', 30))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('sound', 10))
	cursor.execute ("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('motion', 1))
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