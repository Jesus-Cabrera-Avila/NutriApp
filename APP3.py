from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_KEY = "jJ7mu9e8ScW6YatOKKbNFE93fpxcV5E1BLy45NrW"
API_SEARCH = "https://api.nal.usda.gov/fdc/v1/foods/search"

@app.route('/')
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
    app.run(debug=True, port=5002)

