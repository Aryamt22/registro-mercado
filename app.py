from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

usuarios = {}
momentos = ["Desayuno", "Merienda 1", "Almuerzo", "Merienda 2", "Cena"]

@app.route('/')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    usuario = session['usuario']
    inventario = usuarios.get(usuario, {})

    # Calcular días restantes para cada producto y momento
    for producto, data in inventario.items():
        data["dias_restantes"] = {}
        for momento in momentos:
            consumo_diario = data["consumo"].get(momento, 0)
            if consumo_diario > 0:
                data["dias_restantes"][momento] = data["cantidad"] // consumo_diario
            else:
                data["dias_restantes"][momento] = "N/A"
    
    return render_template('index.html', inventario=inventario, momentos=momentos, usuario=usuario)

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    if 'usuario' not in session:
        return jsonify({"error": "No autenticado"}), 401
    
    usuario = session['usuario']
    data = request.json
    producto = data.get("producto")
    cantidad = int(data.get("cantidad", 0))
    consumo = data.get("consumo", {})
    
    if producto and cantidad > 0:
        if usuario not in usuarios:
            usuarios[usuario] = {}
        
        usuarios[usuario][producto] = {"cantidad": cantidad, "consumo": {}}
        for momento in momentos:
            usuarios[usuario][producto]["consumo"][momento] = int(consumo.get(momento, 0))
        
        return jsonify({"message": "Producto agregado", "inventario": usuarios[usuario]})
    
    return jsonify({"error": "Datos inválidos"}), 400

if __name__ == '__main__':
    app.run(debug=True)
