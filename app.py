from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Inventario en memoria (Diccionario)
inventario = {}

momentos = ["Desayuno", "Merienda 1", "Almuerzo", "Merienda 2", "Cena"]

@app.route('/')
def index():
    return render_template("index.html", inventario=inventario, momentos=momentos)

@app.route('/agregar', methods=["POST"])
def agregar():
    data = request.json
    producto = data["producto"]
    cantidad = int(data["cantidad"])
    consumo = {m: int(data["consumo"].get(m, 0)) for m in momentos}
    
    inventario[producto] = {
        "cantidad": cantidad,
        "consumo": consumo
    }
    
    return jsonify({"message": "Producto agregado", "inventario": inventario})

@app.route('/consumir', methods=["POST"])
def consumir():
    data = request.json
    producto = data["producto"]
    momento = data["momento"]
    cantidad = int(data["cantidad"])
    
    if producto in inventario and momento in inventario[producto]["consumo"]:
        inventario[producto]["cantidad"] -= cantidad
        if inventario[producto]["cantidad"] < 0:
            inventario[producto]["cantidad"] = 0
    
    return jsonify({"message": "Consumo registrado", "inventario": inventario})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
