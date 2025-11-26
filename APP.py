from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "Super_secreta_key"

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
                genero = request.form.get("genero", "")

                if genero == "hombre":
                    tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
                else:
                    tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

                resultado["tmb"] = round(tmb, 2)
            except ValueError:
                return "Error: datos inválidos."

    return render_template("calculadoras.html", resultado=resultado)

API_KEY = "jJ7mu9e8ScW6YatOKKbNFE93fpxcV5E1BLy45NrW"
API_SEARCH = "https://api.nal.usda.gov/fdc/v1/foods/search"

TRAD_NUTRIENTES = {
    "Energy": "Energía",
    "Protein": "Proteína",
    "Total lipid (fat)": "Grasa total",
    "Carbohydrate, by difference": "Carbohidratos",
    "Fiber, total dietary": "Fibra",
    "Sugars, total including NLEA": "Azúcares",
    "Calcium, Ca": "Calcio",
    "Iron, Fe": "Hierro",
    "Magnesium, Mg": "Magnesio",
    "Phosphorus, P": "Fósforo",
    "Potassium, K": "Potasio",
    "Sodium, Na": "Sodio",
    "Zinc, Zn": "Zinc",
    "Vitamin C, total ascorbic acid": "Vitamina C",
    "Vitamin D (D2 + D3)": "Vitamina D",
    "Vitamin B-12": "Vitamina B12",
}

def traducir_texto(txt):
    trad = txt.lower()
    trad = trad.replace("raw", "crudo")
    trad = trad.replace("apple", "manzana")
    trad = trad.replace("milk", "leche")
    trad = trad.replace("rice", "arroz")
    return trad.capitalize()

@app.route("/buscar_alimento")
@app.route("/index")
def buscar_alimento():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    food_name = request.form.get("food_name", "").strip()

    if not food_name:
        return render_template("food.html", error="Debes escribir un alimento.")

    params = {
        "api_key": API_KEY,
        "query": food_name
    }

    try:
        resp = requests.get(API_SEARCH, params=params)

        if resp.status_code != 200:
            return render_template("food.html",
                                   error="Error al conectar con la API USDA.")

        data = resp.json()

        if not data.get("foods"):
            return render_template("food.html",
                                   error=f'No se encontró el alimento "{food_name}".')

        food = data["foods"][0]

        nutrientes_es = []
        for n in food.get("foodNutrients", []):
            nombre_original = n.get("nutrientName", "Desconocido")
            nombre_es = TRAD_NUTRIENTES.get(nombre_original, nombre_original)
            nutrientes_es.append({
                "name": nombre_original,
                "name_es": nombre_es,
                "amount": n.get("value", 0),
                "unitName": n.get("unitName", "")
            })

        result = {
            "description": food.get("description"),
            "descripcion_es": traducir_texto(food.get("description", "")),
            "fdcId": food.get("fdcId"),
            "nutrients": nutrientes_es
        }

        return render_template("food.html", result=result)

    except Exception as e:
        return render_template("food.html", error=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
