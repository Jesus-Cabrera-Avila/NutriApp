from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import requests

app = Flask(__name__)
app.secret_key = "Super_secreta_key"

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
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
            archivo.write(f"{correo},{contrasena},{nombre},{apellido},{peso},{altura},{edad},{genero}, {actividad}\n")

        return redirect(url_for('base'))

    return render_template('registro.html')

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
                return redirect(url_for('registro'))

        return render_template('iniciar_sesion.html', error="La contraseña o el Gmail son incorrectos")

    return render_template('iniciar_sesion.html')

@app.route('/objetivos')
def objetivos():
    return render_template('objetivos.html')

@app.route('/recetas')
def recetas():
    return render_template('recetas.html')

@app.route('/cerrar')
def cerrar():
    session.pop('usuario', None)
    return redirect(url_for('inicio'))

@app.route('/p_y_r')
def p_y_r():
    return render_template('p_y_r.html')

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('iniciar_sesion'))

    usuario_sesion = session['usuario']
    datos_usuario = None

    try:
        with open("usuarios.txt", "r", encoding="utf-8") as archivo:
            usuarios = archivo.readlines()
    except FileNotFoundError:
        usuarios = []

    for usuario in usuarios:
        datos = usuario.strip().split(',')
        if len(datos) > 2 and datos[2] == usuario_sesion:
            datos_usuario = {
                "correo": datos[0],
                "nombre": datos[2],
                "apellido": datos[3],
                "peso": datos[4],
                "altura": datos[5],
                "edad": datos[6],
                "genero": datos[7],
                "actividad": datos[8]
            }
            break

    if datos_usuario is None:
        return "No se encontró la información del usuario."

    return render_template('perfil.html', usuario=datos_usuario)

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
                genero = request.form.get("genero", "")

                if genero == "hombre":
                    tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
                else:
                    tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

                resultado["tmb"] = round(tmb, 2)
            except ValueError:
                return "Error: datos inválidos."

    return render_template("calculadoras.html", resultado=resultado)

app.secret_key = "Super_Secreta_Key"

API_KEY = "hWxgeCYhum2YXYilyUj5qqknNllWqUAQKSfS2l8a"
API_SEARCH = "https://api.nal.usda.gov/fdc/v1/foods/search"

TRADUCCIONES = {
    "Protein": "Proteína",
    "Total lipid (fat)": "Grasa total",
    "Carbohydrate, by difference": "Carbohidratos",
    "Energy": "Energía",
    "Sugars, total": "Azúcares totales",
    "Fiber, total dietary": "Fibra dietética total",
    "Calcium, Ca": "Calcio",
    "Iron, Fe": "Hierro",
    "Sodium, Na": "Sodio",
    "Vitamin C, total ascorbic acid": "Vitamina C",
    "Vitamin A, RAE": "Vitamina A",
    "Cholesterol": "Colesterol",
    "Fatty acids, total saturated": "Grasas saturadas",
    "Fatty acids, total trans": "Grasas trans",
    "Water": "Agua"
}

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search_food():
    food_name = request.form.get('food_name', '').strip()

    if not food_name:
        flash("Por favor ingresa un alimento", "error")
        return redirect(url_for('index'))

    try:
        params = {
            "api_key": API_KEY,
            "query": food_name
        }

        resp = requests.get(API_SEARCH, params=params)

        if resp.status_code == 200:
            data = resp.json()

            if not data.get("foods"):
                flash(f'El alimento "{food_name}" no fue encontrado', "error")
                return redirect(url_for('index'))

            food = data["foods"][0]

            nutrientes_traducidos = []
            for n in food.get("foodNutrients", []):
                nombre_original = n.get("nutrientName", "")
                valor = n.get("value", "")
                unidad = n.get("unitName", "")

                nombre_es = TRADUCCIONES.get(nombre_original, nombre_original)

                nutrientes_traducidos.append({
                    "nutrientName": nombre_es,
                    "value": valor,
                    "unitName": unidad
                })

            food_info = {
                "description": food["description"],
                "fdcId": food["fdcId"],
                "brandOwner": food.get("brandOwner", "No disponible"),
                "score": food.get("score", "N/A"),
                "nutrients": nutrientes_traducidos
            }

            return render_template("food.html", food=food_info)

        else:
            flash("Error al buscar el alimento", "error")
            return redirect(url_for('index'))

    except requests.exceptions.RequestException:
        flash("Error al conectar con la API USDA", "error")
        return redirect(url_for('index'))

@app.route('/api')
def home():
    return jsonify({
        "message": "Bienvenido a la API USDA personalizada",
        "uso": "/food/<nombre>"
    })


@app.route('/food/<name>', methods=['GET'])
def food_lookup(name):
    name = name.strip()

    try:
        params = {
            "api_key": API_KEY,
            "query": name
        }

        resp = requests.get(API_SEARCH, params=params)

        if resp.status_code == 200:
            data = resp.json()

            if not data.get("foods"):
                return jsonify({
                    "status": "error",
                    "message": f'El alimento "{name}" no fue encontrado'
                }), 404

            food = data["foods"][0]

            food_info = {
                "description": food["description"],
                "fdcId": food["fdcId"],
                "brandOwner": food.get("brandOwner", "No disponible"),
                "score": food.get("score", "N/A"),
                "nutrients": food.get("foodNutrients", [])
            }

            return jsonify({
                "status": "success",
                "food": food_info
            }), 200

        else:
            return jsonify({
                "status": "error",
                "message": "Error al buscar el alimento"
            }), 500

    except requests.exceptions.RequestException:
        return jsonify({
            "status": "error",
            "message": "Error al conectar con la API USDA"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)

