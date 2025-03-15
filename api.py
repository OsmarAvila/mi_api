from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Base de datos de alimentos completa (valores por cada 100g)
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

factores_actividad = {
    "sedentario": 1.2,
    "poco activo": 1.375,
    "moderado": 1.55,
    "activo": 1.725,
    "muy activo": 1.9
}

def calcular_gasto_calorico(peso, altura, edad, genero, actividad, objetivo):
    """Calcula el gasto calórico y los macronutrientes."""
    
    if genero.lower() == "hombre":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

    get = tmb * factores_actividad.get(actividad, 1.55)

    if objetivo == "perder grasa":
        calorias_diarias = get - 500
    elif objetivo == "ganar músculo":
        calorias_diarias = get + 300
    else:
        calorias_diarias = get

    proteina_total = peso * 3
    grasas_total = peso * 1
    calorias_proteinas = proteina_total * 4
    calorias_grasas = grasas_total * 9
    calorias_carbohidratos = calorias_diarias - (calorias_proteinas + calorias_grasas)
    carbohidratos_total = calorias_carbohidratos / 4

    return calorias_diarias, proteina_total, carbohidratos_total, grasas_total

@app.route("/calcular", methods=["POST"])
def calcular():
    datos = request.json
    try:
        peso = datos["peso"]
        altura = datos["altura"]
        edad = datos["edad"]
        genero = datos["genero"]
        actividad = datos["actividad"]
        objetivo = datos["objetivo"]
    except KeyError:
        return jsonify({"error": "Faltan datos necesarios"}), 400

    calorias_diarias, proteina_total, carbohidratos_total, grasas_total = calcular_gasto_calorico(
        peso, altura, edad, genero, actividad, objetivo
    )

    # Distribuir los macronutrientes según el objetivo
    proteina_por_comida = proteina_total * 0.5  # 50% de la proteína
    grasa_por_comida = grasas_total * 0.2  # 20% de las grasas
    carbohidrato_por_comida = carbohidratos_total * 0.3  # 30% de los carbohidratos

    # Generar menú con las cantidades ajustadas
    menu = {
        "Comida 1": {
            "proteina": {"nombre": "Pollo", "cantidad": f"{proteina_por_comida}g"},
            "carbohidrato": {"nombre": "Avena", "cantidad": f"{carbohidrato_por_comida}g"},
            "grasa": {"nombre": "Palta", "cantidad": f"{grasa_por_comida}g"}
        },
        "Comida 2": {
            "proteina": {"nombre": "Atún enlatado al agua", "cantidad": f"{proteina_por_comida}g"},
            "carbohidrato": {"nombre": "Arroz integral", "cantidad": f"{carbohidrato_por_comida}g"},
            "grasa": {"nombre": "Almendras", "cantidad": f"{grasa_por_comida}g"}
        },
        "Comida 3": {
            "proteina": {"nombre": "Salmón", "cantidad": f"{proteina_por_comida}g"},
            "carbohidrato": {"nombre": "Batata", "cantidad": f"{carbohidrato_por_comida}g"},
            "grasa": {"nombre": "Aceite de oliva", "cantidad": f"{grasa_por_comida}g"}
        }
    }

    return jsonify({
        "mensaje": "Menú generado exitosamente",
        "menu": menu
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
