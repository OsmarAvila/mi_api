from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos de alimentos completa (valores por cada 100g)
alimentos = {
    "proteinas": [
        {"nombre": "Pollo", "cantidad": "100 g", "calorias": 120, "grasa": 2.6, "carbohidratos": 0, "proteina": 22.5},
        {"nombre": "Carne magra", "cantidad": "100 g", "calorias": 135, "grasa": 4.62, "carbohidratos": 0, "proteina": 23},
        {"nombre": "Atún enlatado al agua", "cantidad": "100 g", "calorias": 100, "grasa": 0, "carbohidratos": 0, "proteina": 25},
        {"nombre": "Salmón", "cantidad": "100 g", "calorias": 185, "grasa": 12, "carbohidratos": 1, "proteina": 18.4},
        {"nombre": "Huevo entero", "cantidad": "100 g", "calorias": 66, "grasa": 3.75, "carbohidratos": 1, "proteina": 6.5}
    ],
    "carbohidratos": [
        {"nombre": "Avena", "cantidad": "100 g", "calorias": 389, "grasa": 7, "carbohidratos": 67, "proteina": 14},
        {"nombre": "Arroz integral", "cantidad": "100 g", "calorias": 360, "grasa": 1, "carbohidratos": 77, "proteina": 7},
        {"nombre": "Batata", "cantidad": "100 g", "calorias": 86, "grasa": 0.1, "carbohidratos": 20, "proteina": 2}
    ],
    "grasas": [
        {"nombre": "Palta", "cantidad": "100 g", "calorias": 160, "grasa": 15, "carbohidratos": 8, "proteina": 2},
        {"nombre": "Aceite de oliva", "cantidad": "100 ml", "calorias": 900, "grasa": 100, "carbohidratos": 0, "proteina": 0},
        {"nombre": "Almendras", "cantidad": "100 g", "calorias": 575, "grasa": 49, "carbohidratos": 22, "proteina": 21}
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

def calcular_gasto_calorico(peso, altura, edad, genero, actividad, objetivo):
    """Calcula el GET (Gasto Energético Total) y la distribución de macronutrientes"""
    
    # Cálculo del TMB (Tasa Metabólica Basal)
    if genero.lower() == "hombre":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161

    # Aplicar factor de actividad para obtener el GET
    get = tmb * factores_actividad.get(actividad, 1.55)

    # Ajustar calorías según el objetivo
    if objetivo == "perder grasa":
        calorias_diarias = get - 500
    elif objetivo == "ganar músculo":
        calorias_diarias = get + 300
    else:
        calorias_diarias = get

    # Distribución de macronutrientes
    proteina_total = peso * 3  # 3g de proteína por kg de peso
    grasas_total = peso * 1     # 1g de grasa por kg de peso
    calorias_proteinas = proteina_total * 4  # Calorías de proteínas
    calorias_grasas = grasas_total * 9       # Calorías de grasas
    calorias_carbohidratos = calorias_diarias - (calorias_proteinas + calorias_grasas)  # Resto para carbohidratos
    carbohidratos_total = calorias_carbohidratos / 4  # Convertir calorías a gramos de carbohidratos

    return calorias_diarias, proteina_total, carbohidratos_total, grasas_total

@app.route("/calcular", methods=["POST"])
def calcular():
    """Recibe los datos del usuario y devuelve el cálculo calórico + lista de alimentos"""
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

    # Calcular GET y macronutrientes
    calorias_diarias, proteina_total, carbohidratos_total, grasas_total = calcular_gasto_calorico(
        peso, altura, edad, genero, actividad, objetivo
    )

    return jsonify({
        "calorias_objetivo": calorias_diarias,
        "macronutrientes": {
            "proteina_total_g": proteina_total,
            "carbohidratos_total_g": carbohidratos_total,
            "grasas_total_g": grasas_total
        },
        "alimentos_disponibles": alimentos
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
