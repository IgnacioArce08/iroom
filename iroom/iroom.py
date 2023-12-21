#!/usr/bin/python
# -- coding: utf-8 --

from flask import Flask, url_for, session, render_template, Response, request, flash, redirect, abort, jsonify
from flaskext.mysql import MySQL
import json
import time
import random
import string


mysql = MySQL()

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('IROOM_SETTINGS', silent=True)
mysql.init_app(app)
last_value = [0, 0, 0, 0, 0]


def event_sensor():
    while True:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select valor from sensors where nombre='temperature' order by time desc")
        temperatura = int(cursor.fetchone()[0])
        if temperatura != last_value[0]:
            sensor = {"tipo": "temperatura", "valor": temperatura}
            data_json = json.dumps(sensor)
            print(sensor)
            yield 'data: %s\n\n' % str(data_json)
            last_value[0] = temperatura
            #flash('Actualizado sensor de temperatura')
            
        cursor.execute(
        "select valor from sensors where nombre='humidity' order by time desc")
        humedad = int(cursor.fetchone()[0])
        if humedad != last_value[1]:
            sensor = {"tipo": "humedad", "valor": humedad}
            data_json = json.dumps(sensor)
            print(sensor)
            yield 'data: %s\n\n' % str(data_json)
            last_value[1] = humedad
            #flash('actualizado sensor humedad')
        cursor.execute(
                "select valor from sensors where nombre='light' order by time desc")
        luz = int(cursor.fetchone()[0])
        if luz != last_value[2]:
            sensor = {"tipo": "luz", "valor": luz}
            data_json = json.dumps(sensor)
            print(sensor)
            yield 'data: %s\n\n' % str(data_json)
            last_value[2] = luz
            #flash('Actualizado sensor de luz')
        cursor.execute(
        "select valor from sensors where nombre='sound' order by time desc")
        sonido = int(cursor.fetchone()[0])
        if sonido != last_value[3]:
            sensor = {"tipo": "sonido", "valor": sonido}
            data_json = json.dumps(sensor)
            print(sensor)
            yield 'data: %s\n\n' % str(data_json)
            last_value[3] = sonido
            #flash('Actualizado sensor de sonido')
        cursor.execute(
        "select valor from sensors where nombre='motion' order by time desc")
        movimiento = int(cursor.fetchone()[0])
        if movimiento != last_value[4]:
            sensor = {"tipo": "movimiento", "valor": movimiento}
            print(sensor)
            yield 'data: %s\n\n' % str(data_json)
            last_value[4] = movimiento
            # flash('Actualizado sensor de movimiento)


@app.route('/update_sensor')
def sse_request():
    return Response(event_sensor(), mimetype='text/event-stream')
@app.route('/URL/<codigo>')
def cod(codigo):
    if session['logged_in'] == True:
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute ("select url from codigos where codigos=%s", (codigo))
            conn.commit()
            enlace = cursor.fetchone()[0]
            return redirect (enlace)
        except:
            print("No se ha registrado")
    else:
        return redirect (url_for(login))
    


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/sensors')
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
    color = request.args.get('color')
    red = int('0x' + color[1:3], 16)
    green = int('0x' + color[3:5], 16)
    blue = int('0x' + color[5:7], 16)
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('red', red))
        cursor.execute("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('green', green))
        cursor.execute("""INSERT INTO sensors(nombre, valor) values(%s, %s)""", ('blue', blue))
        conn.commit()
    except mysql.connector.Error as error:
        print("Ha ocurrido un error: ".format(error))
    return render_template('iluminacion.html')


if __name__ == '__main__':
    with app.test_request_context():
        app.debug = True
        app.run(host='0.0.0.0')
