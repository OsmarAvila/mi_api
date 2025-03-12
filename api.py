from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# 📌 Base de datos de alimentos con valores nutricionales (por 100g)
alimentos = {
    "proteínas": {
        "Pollo": {"calorias": 120, "grasa": 2.6, "carbohidratos": 0, "proteina": 22.5},
        "Carne magra": {"calorias": 135, "grasa": 4.62, "carbohidratos": 0, "proteina": 23},
        "Atún enlatado al agua": {"calorias": 100, "grasa": 0, "carbohidratos": 0, "proteina": 25},
        "Salmón": {"calorias": 185, "grasa": 12, "carbohidratos": 1, "proteina": 18.4},
        "Claras de huevo": {"calorias": 50, "grasa": 0.5, "carbohidratos": 1, "proteina": 10},
        "Huevo entero": {"calorias": 66, "grasa": 3.75, "carbohidratos": 1, "proteina": 6.5},
        "Tofu": {"calorias": 110, "grasa": 6.9, "carbohidratos": 1, "proteina": 11},
        "Seitán": {"calorias": 124, "grasa": 1.8, "carbohidratos": 2.9, "proteina": 24.1}
    },
    "carbohidratos": {
        "Avena": {"calorias": 389, "grasa": 7, "carbohidratos": 67, "proteina": 14},
        "Arroz integral": {"calorias": 360, "grasa": 1, "carbohidratos": 77, "proteina": 7},
        "Batata": {"calorias": 86, "grasa": 0.1, "carbohidratos": 20, "proteina": 2},
        "Papa": {"calorias": 77, "grasa": 0, "carbohidratos": 17.47, "proteina": 2}
    },
    "grasas": {
        "Palta": {"calorias": 160, "grasa": 15, "carbohidratos": 8, "proteina": 2},
        "Aceite de oliva": {"calorias": 900, "grasa": 100, "carbohidratos": 0, "proteina": 0},
        "Almendras": {"calorias": 575, "grasa": 49, "carbohidratos": 22, "proteina": 21},
        "Nueces": {"calorias": 654, "grasa": 65, "carbohidratos": 14, "proteina": 15},
        "Mantequilla de maní": {"calorias": 573, "grasa": 50, "carbohidratos": 20, "proteina": 25}
    },
    "verduras": {
        "Espinaca": {"calorias": 23, "grasa": 0.4, "carbohidratos": 4, "proteina": 3},
        "Brócoli": {"calorias": 34, "grasa": 0.4, "carbohidratos": 7, "proteina": 3},
        "Zanahoria": {"calorias": 41, "grasa": 0.1, "carbohidratos": 10, "proteina": 1},
        "Tomate": {"calorias": 18, "grasa": 0.2, "carbohidratos": 3.9, "proteina": 0.9},
        "Pepino": {"calorias": 16, "grasa": 0.1, "carbohidratos": 3.6, "proteina": 0.7},
        "Pimientos": {"calorias": 40, "grasa": 0.3, "carbohidratos": 9, "proteina": 2}
    }
}

@app.route("/generar_menu", methods=["POST"])
def generar_menu():
    datos = request.json
    if not datos:
        return jsonify({"error": "No se enviaron datos"}), 400
    
    peso = datos.get("peso", 70)
    calorias_objetivo = datos.get("calorias", 2500)
    comidas_por_dia = datos.get("comidas_por_dia", 3)
    alergias = datos.get("alergias", [])
    horarios = datos.get("horarios", [])

    proteina_objetivo = 3 * peso
    grasa_objetivo = 1 * peso
    carbohidratos_objetivo = (calorias_objetivo - (proteina_objetivo * 4) - (grasa_objetivo * 9)) // 4

    menu = {}
    for i in range(comidas_por_dia):
        comida = f"Comida {i+1} - {horarios[i] if i < len(horarios) else 'Sin horario definido'}"
        menu[comida] = {}

        for tipo in ["proteínas", "carbohidratos", "grasas", "verduras"]:
            opciones = [a for a in alimentos[tipo] if a not in alergias]
            if opciones:
                alimento_elegido = random.choice(opciones)
                valores = alimentos[tipo][alimento_elegido]

                if tipo == "proteínas":
                    cantidad = (proteina_objetivo // comidas_por_dia) / valores["proteina"] * 100
                elif tipo == "carbohidratos":
                    cantidad = (carbohidratos_objetivo // comidas_por_dia) / valores["carbohidratos"] * 100
                elif tipo == "grasas":
                    cantidad = (grasa_objetivo // comidas_por_dia) / valores["grasa"] * 100
                else:  # Verduras, se asigna un valor estándar de 100g
                    cantidad = 100  

                menu[comida][tipo.capitalize()] = {
                    "Alimento": alimento_elegido,
                    "Cantidad (g)": round(cantidad, 1),
                    "Calorías": round(valores["calorias"] * (cantidad / 100), 1),
                    "Proteína (g)": round(valores["proteina"] * (cantidad / 100), 1),
                    "Carbohidratos (g)": round(valores["carbohidratos"] * (cantidad / 100), 1),
                    "Grasas (g)": round(valores["grasa"] * (cantidad / 100), 1)
                }

    return jsonify({"menu": menu, "calorias_totales": calorias_objetivo})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render asigna un puerto automáticamente
    app.run(host="0.0.0.0", port=port, debug=True)
