from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/inicio')
def inicio():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        peso = request.form.get('peso')
        altura = request.form.get('altura')
        actividad = request.form.get('actividad')
        genero = request.form.get('genero')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        edad = request.form.get('edad')

        with open("usuarios.txt", "a") as archivo:
            archivo.write(f"{correo},{contraseña},{nombre},{apellido},{peso},{altura},{edad},{genero}\n")

        return redirect(url_for('base.html'))

    return render_template('inicio.html')

@app.route('/iniciar secion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        try:
            with open("usuarios.txt", "r") as archivo:
                usuarios = archivo.readlines()
        except FileNotFoundError:
            usuarios = []

        for usuario in usuarios:
            datos = usuario.strip().split(',')
            if len(datos) >= 2 and correo == datos[0] and contraseña == datos[1]:
                session['usuario'] = datos[2]  
                return redirect(url_for('inicio'))

        return render_template('iniciar cesion.html', error="La contraseña o el Gmail son incorrectos")

    return render_template('iniciar cesion.html')


@app.route('/objetivos')
def objetivos():
    return render_template('objetivos.html')

@app.route('/cerrar')
def cerrar():
    session.pop('usuario', None)
    return redirect(url_for('inicio'))

@app.route('/p y r')
def P_R():
    return render_template('p y r.html')


if __name__ == '__main__':
    app.run(debug=True)

