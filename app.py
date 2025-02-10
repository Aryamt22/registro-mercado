from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

inventario = {}
momentos = ["Desayuno", "Merienda 1", "Almuerzo", "Merienda 2", "Cena"]

@app.route("/")
def index():
    return render_template("index.html", inventario=inventario, momentos=momentos, usuario="aryam")

@app.route("/agregar", methods=["POST"])
def agregar():
    data = request.json
    producto = data.get("producto")
    cantidad = int(data.get("cantidad", 0))
    consumo = data.get("consumo", {})

    if not producto or cantidad <= 0:
        return jsonify({"error": "Producto o cantidad inválidos"}), 400

    if producto not in inventario:
        inventario[producto] = {"cantidad": cantidad, "consumo": {m: 0 for m in momentos}}
    else:
        inventario[producto]["cantidad"] += cantidad

    for momento in momentos:
        inventario[producto]["consumo"][momento] = int(consumo.get(momento, 0))

    return jsonify({"message": "Producto agregado", "inventario": inventario})

@app.route("/logout")
def logout():
    return "Sesión cerrada"

if __name__ == "__main__":
    app.run(debug=True)
