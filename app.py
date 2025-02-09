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
    
    # Calcular días restantes por producto
    for producto, data in inventario.items():
        consumo_diario_total = sum(data["consumo"].values())
        data["dias_restantes"] = (data["cantidad"] // consumo_diario_total) if consumo_diario_total > 0 else "∞"

    return render_template('index.html', inventario=inventario, momentos=momentos, usuario=usuario)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        if usuario:
            session['usuario'] = usuario
            if usuario not in usuarios:
                usuarios[usuario] = {}
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    if 'usuario' not in session:
        return jsonify({"error": "No autenticado"}), 401
    usuario = session['usuario']
    data = request.json
    producto = data.get("producto")
    cantidad = int(data.get("cantidad", 0))
    
    if not producto or cantidad <= 0:
        return jsonify({"error": "Datos inválidos"}), 400

    if usuario not in usuarios:
        usuarios[usuario] = {}

    if producto not in usuarios[usuario]:
        usuarios[usuario][producto] = {"cantidad": 0, "consumo": {m: 0 for m in momentos}}

    usuarios[usuario][producto]["cantidad"] += cantidad
    return jsonify({"message": "Producto agregado", "inventario": usuarios[usuario]})

@app.route('/registrar_consumo', methods=['POST'])
def registrar_consumo():
    if 'usuario' not in session:
        return jsonify({"error": "No autenticado"}), 401
    usuario = session['usuario']
    data = request.json
    producto = data.get("producto")
    momento = data.get("momento")
    cantidad = int(data.get("cantidad", 0))

    if not producto or not momento or cantidad <= 0:
        return jsonify({"error": "Datos inválidos"}), 400

    if usuario not in usuarios or producto not in usuarios[usuario]:
        return jsonify({"error": "Producto no registrado"}), 400

    if momento not in usuarios[usuario][producto]["consumo"]:
        return jsonify({"error": "Momento de consumo no válido"}), 400

    if usuarios[usuario][producto]["cantidad"] < cantidad:
        return jsonify({"warning": f"No hay suficiente {producto} en inventario."})

    usuarios[usuario][producto]["cantidad"] -= cantidad
    usuarios[usuario][producto]["consumo"][momento] += cantidad

    return jsonify({"message": "Consumo registrado", "inventario": usuarios[usuario]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
