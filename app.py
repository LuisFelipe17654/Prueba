from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = "clave_super_secreta"  

def conexion_db():
    return mysql.connector.connect(
        host="TU_USUARIO.mysql.pythonanywhere-services.com",
        user="TU_USUARIO",
        password="TU_PASSWORD",
        database="TU_USUARIO$joyeria"
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
        contrasena_hash = generate_password_hash(contrasena)

        query = "INSERT INTO usuarios (nombre, email, contrasena) VALUES (%s, %s, %s)"
        values = (nombre, email, contrasena_hash)
        cursor.execute(query, values)
        conn.commit()

        flash("✅ Registro exitoso", "success")
        return redirect(url_for('index'))

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
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios")
        usuarios = cursor.fetchall()
        return render_template('index.html', usuarios=usuarios)
    except Error as e:
        flash("❌ Error: " + str(e), "danger")
        return redirect(url_for('index'))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    app.run()
