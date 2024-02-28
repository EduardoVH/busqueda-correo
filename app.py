from flask import Flask, render_template, request, redirect, url_for, flash
import re
import pandas as pd

app = Flask(__name__, template_folder='.')
# app.secret_key = 'tu_clave_secreta'

def validar_contrasena(contrasena):
    # minimo 8 caracteres, maximo 10-15, al menos una mayuscula, una minuscula, un digito, un caracter especial, sin espacios en blanco
    patron = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$"
    return re.match(patron, contrasena)

def cargar_datos_excel():
    return pd.read_excel('datos.xlsx')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if validar_contrasena(contrasena):
            return redirect(url_for('buscar'))
        else:
            flash('Contraseña no válida. Asegúrate de seguir los criterios de contraseña.')
    return render_template('login.html')

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        correo = request.form['correo']
        datos = cargar_datos_excel()

        datos.columns = datos.columns.str.strip()

        resultado = datos[datos['Correo'] == correo]
        return render_template('resultado_busqueda.html', resultado=resultado)
    return render_template('buscar.html')



if __name__ == '__main__':
    app.run(debug=True)
