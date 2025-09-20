from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = "clave_super_secreta"  # Necesaria para usar flash

# Configuración de conexión a MySQL
def conexion_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # cámbialo por tu usuario
        password="",        # tu contraseña
        database="prueba"  # la base creada
    )

@app.route('/')
def index():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    email = request.form['email']
    contrasena = request.form['contrasena']

    try:
        conn = conexion_db()
        cursor = conn.cursor()

        # Encriptamos la contraseña
        contrasena_hash = generate_password_hash(contrasena)

        query = "INSERT INTO usuarios (nombre, email, contrasena) VALUES (%s, %s, %s)"
        values = (nombre, email, contrasena_hash)
        cursor.execute(query, values)
        conn.commit()

        flash("✅ Registro exitoso, bienvenido " + nombre, "success")
        return redirect(url_for('principal'))

    except Error as e:
        flash("❌ Error al registrar: " + str(e), "danger")
        return redirect(url_for('index'))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/principal')
def principal():
    try:
        conn = conexion_db()
        cursor = conn.cursor(dictionary=True)  # <- esto devuelve dict en lugar de tuplas

        cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios")
        usuarios = cursor.fetchall()

        return render_template('index.html', usuarios=usuarios)

    except Error as e:
        flash("❌ Error al obtener usuarios: " + str(e), "danger")
        return redirect(url_for('index'))

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
