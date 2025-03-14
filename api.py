from flask import Flask, request, jsonify
from waitress import serve

app = Flask(__name__)

# Base de datos de alimentos completa
alimentos = {
    "proteinas": [
        {"nombre": "Pollo", "calorias": 120, "grasa": 2.6, "carbohidratos": 0, "proteina": 22.5},
        {"nombre": "Carne magra", "calorias": 135, "grasa": 4.62, "carbohidratos": 0, "proteina": 23},
        {"nombre": "Atún enlatado al agua", "calorias": 100, "grasa": 0, "carbohidratos": 0, "proteina": 25},
        {"nombre": "Salmón", "calorias": 185, "grasa": 12, "carbohidratos": 1, "proteina": 18.4},
        {"nombre": "Huevo entero", "calorias": 66, "grasa": 3.75, "carbohidratos": 1, "proteina": 6.5},
        {"nombre": "Tofu", "calorias": 110, "grasa": 6.9, "carbohidratos": 1, "proteina": 11}
    ],
    "carbohidratos": [
        {"nombre": "Avena", "calorias": 389, "grasa": 7, "carbohidratos": 67, "proteina": 14},
        {"nombre": "Arroz integral", "calorias": 360, "grasa": 1, "carbohidratos": 77, "proteina": 7},
        {"nombre": "Papa", "calorias": 77, "grasa": 0, "carbohidratos": 17.47, "proteina": 2},
        {"nombre": "Batata", "calorias": 86, "grasa": 0.1, "carbohidratos": 20, "proteina": 2}
    ],
    "grasas": [
        {"nombre": "Palta", "calorias": 160, "grasa": 15, "carbohidratos": 8, "proteina": 2},
        {"nombre": "Aceite de oliva", "calorias": 900, "grasa": 100, "carbohidratos": 0, "proteina": 0},
        {"nombre": "Almendras", "calorias": 575, "grasa": 49, "carbohidratos": 22, "proteina": 21}
    ]
}

# Factores de actividad física
factores_actividad = {
    "sedentario": 1.2,
    "poco activo": 1.375,
    "moderado": 1.55,
    "activo": 1.725,
    "muy activo": 1.9
}

@app.route("/generar_menu", methods=["POST"])
def generar_menu():
    datos = request.json
    peso = datos.get("peso")
    altura = datos.get("altura")
    edad = datos.get("edad")
    genero = datos.get("genero")
    actividad = datos.get("actividad")
    objetivo = datos.get("objetivo")
    comidas_por_dia = datos.get("comidas_por_dia")

    if None in [peso, altura, edad, genero, actividad, objetivo, comidas_por_dia]:
        return jsonify({"error": "Faltan datos necesarios"}), 400

    # Calcular TMB
    if genero.lower() == "hombre":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

    # Calcular GET
    get = tmb * factores_actividad.get(actividad, 1.55)

    # Ajustar calorías según objetivo
    if objetivo == "perder grasa":
        calorias_diarias = get - 500
    elif objetivo == "ganar músculo":
        calorias_diarias = get + 300
    else:
        calorias_diarias = get

    # Distribución de macronutrientes
    proteinas_total = peso * 3  # 3g/kg
    grasas_total = peso * 1  # 1g/kg
    calorias_proteinas = proteinas_total * 4
    calorias_grasas = grasas_total * 9
    calorias_carbohidratos = calorias_diarias - (calorias_proteinas + calorias_grasas)
    carbohidratos_total = calorias_carbohidratos / 4

    # Crear menú básico
    menu = {
        "desayuno": [alimentos["proteinas"][0], alimentos["carbohidratos"][0], alimentos["grasas"][0]],
        "almuerzo": [alimentos["proteinas"][1], alimentos["carbohidratos"][1], alimentos["grasas"][1]],
        "cena": [alimentos["proteinas"][2], alimentos["carbohidratos"][2], alimentos["grasas"][2]],
    }
    if comidas_por_dia == 4:
        menu["merienda"] = [alimentos["proteinas"][3], alimentos["carbohidratos"][3], alimentos["grasas"][0]]
    elif comidas_por_dia == 5:
        menu["merienda"] = [alimentos["proteinas"][3], alimentos["carbohidratos"][3], alimentos["grasas"][0]]
        menu["colación"] = [alimentos["proteinas"][4], alimentos["carbohidratos"][2], alimentos["grasas"][1]]

    return jsonify({
        "calorias_diarias": calorias_diarias,
        "macronutrientes": {
            "proteina": proteinas_total,
            "grasas": grasas_total,
            "carbohidratos": carbohidratos_total
        },
        "menu": menu
    })

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
