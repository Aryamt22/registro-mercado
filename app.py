from flask import Flask, render_template, request, redirect, url_for, jsonify
import os

app = Flask(__name__)

# Simulación de base de datos en memoria
inventario = {}
momentos = ["Desayuno", "Merienda 1", "Almuerzo", "Merienda 2", "Cena"]


@app.route("/")
def index():
    return render_template("index.html", inventario=inventario, momentos=momentos, usuario="Usuario")


@app.route("/agregar", methods=["POST"])
def agregar_producto():
    data = request.json
    producto = data.get("producto")
    cantidad = int(data.get("cantidad", 0))
    consumo = data.get("consumo", {})

    if not producto or cantidad <= 0:
        return jsonify({"error": "Producto inválido o cantidad incorrecta"}), 400

    if producto in inventario:
        inventario[producto]["cantidad"] += cantidad
    else:
        inventario[producto] = {"cantidad": cantidad, "consumo": consumo}

    return jsonify({"message": "Producto agregado", "inventario": inventario})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Obtiene el puerto asignado por Render
    app.run(host="0.0.0.0", port=port, debug=True)
