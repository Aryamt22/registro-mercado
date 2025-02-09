from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

inventario = {}
momentos = ["Desayuno", "Merienda 1", "Almuerzo", "Merienda 2", "Cena"]

@app.route('/')
def home():
    return render_template('index.html', inventario=inventario, momentos=momentos)

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    data = request.json
    producto = data.get("producto")
    cantidad = int(data.get("cantidad", 0))
    consumo = data.get("consumo", {})
    
    if producto and cantidad > 0:
        inventario[producto] = {"cantidad": cantidad, "consumo": {}}
        for momento in momentos:
            inventario[producto]["consumo"][momento] = int(consumo.get(momento, 0))
        return jsonify({"message": "Producto agregado", "inventario": inventario})
    return jsonify({"error": "Datos inválidos"}), 400

@app.route('/registrar_consumo', methods=['POST'])
def registrar_consumo():
    data = request.json
    producto = data.get("producto")
    if producto in inventario:
        total_consumo = sum(inventario[producto]["consumo"].values())
        inventario[producto]["cantidad"] -= total_consumo
        if inventario[producto]["cantidad"] <= 0:
            return jsonify({"warning": f"{producto} se ha agotado. Debes comprar más."})
        return jsonify({"message": "Consumo registrado", "inventario": inventario})
    return jsonify({"error": "Producto no registrado"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
