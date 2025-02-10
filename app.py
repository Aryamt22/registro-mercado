from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Simulación de inventario en memoria
inventario = {}

# Momentos del día para registrar consumo
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
        return jsonify({"error": "Datos inválidos"}), 400

    if producto in inventario:
        inventario[producto]["cantidad"] += cantidad
    else:
        inventario[producto] = {"cantidad": cantidad, "consumo": {momento: int(consumo.get(momento, 0)) for momento in momentos}}

    return jsonify({"message": "Producto agregado", "inventario": inventario})


@app.route("/logout")
def logout():
    return redirect(url_for("index"))  # Simulación de logout


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
