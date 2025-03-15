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

# Factores de actividad física
factores_actividad = {
    "sedentario": 1.2,
    "poco activo": 1.375,
    "moderado": 1.55,
    "activo": 1.725,
    "muy activo": 1.9
}

def calcular_porciones(macro_total, alimento, tipo):
    if tipo == "proteina":
        return round((macro_total / alimento["proteina"]) * 100, 2)
    elif tipo == "carbohidrato":
        return round((macro_total / alimento["carbohidratos"]) * 100, 2)
    elif tipo == "grasa":
        return round((macro_total / alimento["grasa"]) * 100, 2)
    return 100

def generar_menu_personalizado(calorias_diarias, comidas_por_dia, proteina_total, carbohidratos_total, grasas_total):
    calorias_por_comida = calorias_diarias / comidas_por_dia
    menu = {}
    
    for i in range(comidas_por_dia):
        proteina = random.choice(alimentos["proteinas"])
        carbohidrato = random.choice(alimentos["carbohidratos"])
        grasa = random.choice(alimentos["grasas"])
        
        porcion_proteina = calcular_porciones(proteina_total / comidas_por_dia, proteina, "proteina")
        porcion_carbohidrato = calcular_porciones(carbohidratos_total / comidas_por_dia, carbohidrato, "carbohidrato")
        porcion_grasa = calcular_porciones(grasas_total / comidas_por_dia, grasa, "grasa")
        
        menu[f"Comida {i+1}"] = {
            "proteina": {"nombre": proteina["nombre"], "cantidad": f"{porcion_proteina}g"},
            "carbohidrato": {"nombre": carbohidrato["nombre"], "cantidad": f"{porcion_carbohidrato}g"},
            "grasa": {"nombre": grasa["nombre"], "cantidad": f"{porcion_grasa}g"},
        }
    
    return menu

# Ruta principal
@app.route("/", methods=["GET"])
def home():
    return "¡El servidor está funcionando!"

# Ruta para generar menú
@app.route("/generar_menu", methods=["POST"])
def generar_menu():
    datos = request.json
    try:
        peso = datos["peso"]
        altura = datos["altura"]
        edad = datos["edad"]
        genero = datos["genero"]
        actividad = datos["actividad"]
        objetivo = datos["objetivo"]
        comidas_por_dia = datos["comidas_por_dia"]
    except KeyError:
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

    # Cálculo de macronutrientes
    proteina_total = peso * 3  # 3g/kg
    grasas_total = peso * 1  # 1g/kg
    calorias_proteinas = proteina_total * 4
    calorias_grasas = grasas_total * 9
    calorias_carbohidratos = calorias_diarias - (calorias_proteinas + calorias_grasas)
    carbohidratos_total = calorias_carbohidratos / 4

    # Generar menú con porciones exactas
    menu_personalizado = generar_menu_personalizado(calorias_diarias, comidas_por_dia, proteina_total, carbohidratos_total, grasas_total)
    
    return jsonify({
        "mensaje": "Menú generado exitosamente",
        "menu": menu_personalizado,
        "nota": "Todas las cantidades de alimentos están basadas en valores por cada 100 gramos."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
