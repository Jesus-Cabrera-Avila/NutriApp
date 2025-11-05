from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/objetivoss')
def inicio():
    return render_template('objetivoss.html')


if __name__ == '__main__':
    app.run(debug=True)