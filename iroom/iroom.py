#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, session, render_template, Response, request, flash, redirect, abort, jsonify
from flaskext.mysql import MySQL
import json
import time
import random
import string


mysql = MySQL()

app = Flask(_name_)
app.config.from_object(_name_)
app.config.from_envvar('IROOM_SETTINGS', silent=True)
mysql.init_app(app)
last_value = [0,0,0,0,0]

def event_sensor():
	while True:
		conn = mysql.connect()
		cursor = conn.cursor()

		sensors = [
			('temperature', 'temperatura'),
			('humidity', 'humedad'),
			('light', 'luz'),
			('sound', 'sonido'),
			('motion', 'movimiento')
        ]

		for index, (sensor_name, translated_name) in enumerate(sensors):
			cursor.execute(f"SELECT valor FROM sensors WHERE nombre = '{sensor_name}' ORDER BY time DESC")
			sensor_value = int(cursor.fetchone()[0])

			if sensor_value != last_value[index]:
				sensor = {"tipo": translated_name, "valor": sensor_value}
				data_json = json.dumps(sensor)
				print(sensor)
				yield 'data: %s\n\n' % str(data_json)
				last_value[index] = sensor_value

def generate_short_code(url):
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM urls WHERE short_code = %s", (code,))
        if cursor.fetchone()[0] == 0:
            break
    return code

	   
@app.route('/update_sensor')
def sse_request():	  
	return Response(event_sensor(), mimetype='text/event-stream')
	  
@app.route('/')
def main(): 
	return render_template('index.html')
		
@app.route('/sensors')

#	PARTE 2: INSERTE AQUÍ EL CÓDIGO DE LA FUNCION SENSORS PARA REDIRIGIR A LA VISTA sensors.html 
#	CUANDO SE RECIBE UN GET A /sensors

def sensors():
	return render_template('sensors.html')  


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('Has entrado en la sesion')
			return redirect(url_for('sensors'))
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('Has salido de la sesion')
	return redirect(url_for('main'))


@app.route('/iluminacion')
def iluminacion():
	return render_template('iluminacion.html')


@app.route('/setcolor', methods=['GET'])
def setcolor():
	
	#	PARTE 3: INSERTE AQUI EL CÓDIGO PARA GUARDAR EL COLOR DE LA BASE DE DATOS 
	#	CUANDO SE RECIBE DESDE EL CLIENTE POR AJAX

	color = request.args.get('color')
	red = int('0x'+color[1:3], 16)
	blue= int('0x'+color[3:5], 16)
	green= int('0x'+color[5:7], 16)
	conn = mysql.connect()
	cursor = conn.cursor()
	try:
		cursor.execute ("INSERT INTO sensors (nombre, valor)" "VALUES(%s, %s)", ('red', red))
		cursor.execute ("INSERT INTO sensors (nombre, valor)" "VALUES(%s, %s)", ('green', green))
		cursor.execute ("INSERT INTO sensors (nombre, valor)" "VALUES(%s, %s)", ('blue', blue))
		conn.commit()
	except Exception:
		print ('Error al insertar en base de datos')
		conn.rollback()
	finally:
		cursor.close()
		conn.close()

	# Devolver una respuesta porque si no da error
	return 'Color guardado en la base de datos'
	
@app.route('/add-url', methods=['POST'])
def add_url():
    original_url = request.form['url']
    shortened_code = generate_short_code(original_url)
    
    # Conecta a la base de datos y guarda la URL con su código corto
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO urls (original_url, short_code) VALUES (%s, %s)", (original_url, shortened_code))
        conn.commit()
    except Exception as e:
        print('Error al insertar en la base de datos:', e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    # Redirigir al usuario a una página donde se muestre la URL acortada
    return redirect(url_for('show_short_url', short_code=shortened_code))

@app.route('/<short_code>')
def redirect_to_original(short_code):
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT original_url FROM urls WHERE short_code = %s", (short_code,))
        result = cursor.fetchone()
        if result is None:
            return abort(404)  # Si no se encuentra el código, muestra un error 404
        original_url = result[0]
    except Exception as e:
        print('Error al consultar la base de datos:', e)
        return abort(500)  # Error interno del servidor
    finally:
        cursor.close()
        conn.close()

    return redirect(original_url)

@app.route('/show-short-url/<short_code>')
def show_short_url(short_code):
    # Aquí iría la lógica para mostrar la URL acortada
    return render_template('show_short_url.html', short_code=short_code)


if __name__=='_main_':
	with app.test_request_context():
		app.debug = True
		app.run(host ='0.0.0.0')