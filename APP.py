from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/objetivos')
def objetivos():
    return render_template('objetivos.html')

@app.route('/p y r')
def P_R():
    return render_template('p y r.html')


if __name__ == '__main__':
    app.run(debug=True)