
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Crear la base de datos
def crear_base_datos():
    conexion = sqlite3.connect("deportivo.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            deporte TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    """)

    conexion.commit()  # guardar cambios
    conexion.close()   # cerrar la conexión


# Mostrar las inscripciones registradas
@app.route("/")
def inicio():
    conexion = sqlite3.connect("deportivo.db")
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM inscripciones")
    inscripciones = cursor.fetchall()

    conexion.close()

    return render_template("index.html", inscripciones=inscripciones)


# Agregar una inscripción
@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    deporte = request.form["deporte"]
    categoria = request.form["categoria"]

    conexion = sqlite3.connect("deportivo.db")
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO inscripciones
        (nombre, edad, deporte, categoria)
        VALUES (?, ?, ?, ?)
    """, (
        nombre,
        edad,
        deporte,
        categoria
    ))

    conexion.commit()
    conexion.close()

    return redirect("/")


# ==================================================
# AGREGADO: ELIMINAR UNA INSCRIPCION
# ==================================================
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = sqlite3.connect("deportivo.db")
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM inscripciones WHERE id = ?",
        (id,)
    )

    conexion.commit()  # guardar los cambios
    conexion.close()   # cerrar la conexión

    return redirect("/")  # regresar a las inscripciones


# Consultar horarios
@app.route("/horarios")
def horarios():
    return render_template("horarios.html")


# Ejecutar la aplicación
if __name__ == "__main__":
    crear_base_datos()
    app.run(debug=True)
