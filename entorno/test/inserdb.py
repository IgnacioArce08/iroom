#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import mysql.connector

def insertar_en_base_de_datos(sensor, valor):
    try:
        with mysql.connector.connect(host="localhost", user="nacho", passwd="@Nacho08", db="iroom") as db:
            with db.cursor(buffered=True) as cursor:
                cursor.execute("INSERT INTO sensors(nombre, valor) VALUES (%s, %s)", (sensor, str(valor)))
                db.commit()
        print("Datos insertados correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al escribir en la base de datos: {err}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py <sensor> <valor>")
        sys.exit(1)

    sensor = sys.argv[1]
    valor = sys.argv[2]

    insertar_en_base_de_datos(sensor, valor)
