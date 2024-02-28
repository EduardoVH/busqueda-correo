from flask import Flask, render_template, request, redirect, url_for, flash
import re
import pandas as pd

app = Flask(__name__, template_folder='.')
app.secret_key = 'tu_clave_secreta'  # Clave secreta para sesiones

# Expresión regular para validar la contraseña
def validar_contrasena(contrasena):
    # Mínimo 8 caracteres, máximo 10-15, al menos una mayúscula, una minúscula, un dígito, un carácter especial, sin espacios en blanco
    patron = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$"
    return re.match(patron, contrasena)

# Cargar datos del archivo Excel
def cargar_datos_excel():
    return pd.read_excel('datos.xlsx')

# Ruta para la página de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        # Validar usuario y contraseña aquí (puedes implementarlo según tus necesidades)
        # Por ahora, solo se verifica la contraseña
        if validar_contrasena(contrasena):
            # Redirigir a la página de búsqueda si la contraseña es válida
            return redirect(url_for('buscar'))
        else:
            flash('Contraseña no válida. Asegúrate de seguir los criterios de contraseña.')
    return render_template('login.html')

# Ruta para la página de búsqueda
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        correo = request.form['correo']
        # Cargar datos del archivo Excel
        datos = cargar_datos_excel()

        # Eliminar espacios en blanco alrededor de los nombres de las columnas
        datos.columns = datos.columns.str.strip()

        # Filtrar datos según el correo
        resultado = datos[datos['Correo'] == correo]
        return render_template('resultado_busqueda.html', resultado=resultado)
    return render_template('buscar.html')



if __name__ == '__main__':
    app.run(debug=True)
