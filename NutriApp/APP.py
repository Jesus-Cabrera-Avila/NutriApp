from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route('/')
def inicio():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)