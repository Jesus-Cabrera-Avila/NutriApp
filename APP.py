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

        with open("usuarios.txt", "a") as archivo:
            archivo.write(f"{correo},{contraseña},{nombre},{apellido},{peso},{altura},{edad},{genero}\n")

        return redirect(url_for('base.html'))

    return render_template('inicio.html')


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
