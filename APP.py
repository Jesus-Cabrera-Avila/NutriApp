from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta"

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '')
        apellido = request.form.get('apellido', '')
        peso = request.form.get('peso', '')
        altura = request.form.get('altura', '')
        actividad = request.form.get('actividad', '')
        genero = request.form.get('genero', '')
        correo = request.form.get('correo', '')
        contrasena = request.form.get('contraseña', '')  
        edad = request.form.get('edad', '')

        with open("usuarios.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"{correo},{contrasena},{nombre},{apellido},{peso},{altura},{edad},{genero}\n")

        return redirect(url_for('base'))

    return render_template('inicio.html')

@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        correo = request.form.get('correo', '')
        contrasena = request.form.get('contraseña', '')

        try:
            with open("usuarios.txt", "r", encoding="utf-8") as archivo:
                usuarios = archivo.readlines()
        except FileNotFoundError:
            usuarios = []

        for usuario in usuarios:
            datos = usuario.strip().split(',')
            if len(datos) >= 2 and correo == datos[0] and contrasena == datos[1]:
                session['usuario'] = datos[2] if len(datos) > 2 else correo
                return redirect(url_for('inicio'))

        return render_template('iniciar_sesion.html', error="La contraseña o el Gmail son incorrectos")

    return render_template('iniciar_sesion.html')

@app.route('/objetivos')
def objetivos():
    return render_template('objetivos.html')

@app.route('/cerrar')
def cerrar():
    session.pop('usuario', None)
    return redirect(url_for('inicio'))

@app.route('/p_y_r')
def p_y_r():
    return render_template('p_y_r.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/calculadoras', methods=["GET", "POST"])
def calculadoras():
    resultado = {}

    if request.method == "POST":
        calculadora = request.form.get("calculadora", "")

        if calculadora == "imc":
            try:
                peso = float(request.form.get("peso", 0))
                altura = float(request.form.get("altura", 0)) / 100.0
                if altura <= 0:
                    return "Error: altura no válida."
                imc = peso / (altura ** 2)
                resultado["imc"] = round(imc, 2)
            except ValueError:
                return "Error: datos inválidos."
            
        elif calculadora == "tmb":
            try:
                peso = float(request.form.get("peso", 0))
                altura = float(request.form.get("altura", 0))
                edad = int(request.form.get("edad", 0))
                sexo = request.form.get("sexo", "").lower()

                if sexo == "hombre":
                    tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
                else:
                    tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

                resultado["tmb"] = round(tmb, 2)

            except ValueError:
                return "Error: por favor ingresa peso, altura y edad válidos."
            
        elif calculadora == "gct":
            try:
                peso = float(request.form.get("peso", 0))
                altura = float(request.form.get("altura", 0))
                edad = int(request.form.get("edad", 0))
                sexo = request.form.get("sexo", "").lower()
                factor = float(request.form.get("actividad", 1.2))

                if sexo == "hombre":
                    tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
                else:
                    tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

                gct = tmb * factor
                resultado["gct"] = round(gct, 2)

            except ValueError:
                return "Error: verifica que ingresaste datos válidos."
            
        elif calculadora == "peso_ideal":
            try:
                sexo = request.form.get("sexo", "")
                edad = float(request.form.get("edad", 0))
                peso = float(request.form.get("peso", 0))
                altura_cm = float(request.form.get("altura", 0))

                if altura_cm <= 0:
                    return "Error: la altura no puede ser 0 o negativa."

                altura_m = altura_cm / 100.0

                peso_ideal = 22 * (altura_m ** 2)

                resultado["peso_ideal"] = round(peso_ideal, 2)

            except ValueError:
                return "Error: ingresa solo números válidos."
            
        elif calculadora == "macros":
            try:
                sexo = request.form.get("sexo", "").lower()
                edad = int(request.form.get("edad", 0))
                peso = float(request.form.get("peso", 0))
                altura = float(request.form.get("altura", 0))
                actividad = request.form.get("actividad", "")
                objetivo = request.form.get("objetivo", "")

                if altura <= 0 or peso <= 0 or edad <= 0:
                    return "Error: los datos no pueden ser 0 o negativos."

                if sexo == "hombre":
                    tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
                else:
                    tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

                factores = {
                    "sedentario": 1.2,
                    "principiante": 1.375,
                    "intermedio": 1.55,
                    "avanzado": 1.725
                }

                factor = factores.get(actividad, 1.2)

                cal_mantenimiento = tmb * factor

                if objetivo == "ganar masa muscular":
                    cal_objetivo = cal_mantenimiento + 300
                elif objetivo == "bajar de peso":
                    cal_objetivo = cal_mantenimiento - 300
                else:
                    cal_objetivo = cal_mantenimiento

                proteinas = peso * 2
                grasas = peso * 0.8
                carbohidratos = (cal_objetivo - (proteinas * 4 + grasas * 9)) / 4

                resultado["calorias_objetivo"] = round(cal_objetivo, 2)
                resultado["proteinas"] = round(proteinas, 2)
                resultado["grasas"] = round(grasas, 2)
                resultado["carbohidratos"] = round(carbohidratos, 2)

            except ValueError:
                return "Error: ingresa solo números válidos."


    return render_template("calculadoras.html", resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
