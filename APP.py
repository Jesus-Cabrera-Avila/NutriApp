from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import requests

app = Flask(__name__)
app.secret_key = "super_dupe_mega_ultra_milti_key_por_favor_no_robar"

@app.route('/')
def base():
    return render_template('base.html')

usuario = {}

@app.route("/registro", methods=["GET", "POST"])
def registro():
    global usuario

    if request.method == "POST":
        usuario = {
            "edad": request.form.get("edad"),
            "peso": request.form.get("peso"),
            "altura": request.form.get("altura"),
            "actividad": request.form.get("actividad"),
            "genero": request.form.get("genero"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }

        return redirect("/iniciar_sesion")

    return render_template("registro.html")

@app.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if usuario and email == usuario["email"] and password == usuario["password"]:
            session["usuario"] = email
            return redirect("/perfil")
        else:
            return render_template("iniciar_sesion.html", error="Correo o contraseña incorrectos")

    return render_template("iniciar_sesion.html")

@app.route("/perfil")
def perfil():
    if "usuario" not in session:
        return redirect("/iniciar_sesion")

    return render_template("perfil.html", usuario=usuario)

@app.route("/cerrar")
def cerrar():
    session.clear()
    return redirect("/")

@app.route('/objetivos')
def objetivos():
    return render_template('objetivos.html')

@app.route('/recetas')
def recetas():
    return render_template('recetas.html')

@app.route('/p_y_r')
def p_y_r():
    return render_template('p_y_r.html')

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
        "message": "Bienvenido",
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


