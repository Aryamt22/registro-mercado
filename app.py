from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

usuarios = {}
momentos = ["Desayuno", "Merienda 1", "Almuerzo", "Merienda 2", "Cena"]

# Habilitar sum() en Jinja
app.jinja_env.globals.update(sum=sum)

@app.route('/')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    usuario = session['usuario']
    inventario = usuarios.get(usuario, {})

    # Calcular días restantes en el servidor
    for producto, data in inventario.items():
        total_consumo = sum(data["consumo"].values()) if data["consumo"] else 0
        data["dias_restantes"] = (data["cantidad"] // total_consumo) if total_consumo > 0 else 1

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
    consumo = data.get("consumo", {})
    
    if producto and cantidad > 0:
        if usuario not in usuarios:
            usuarios[usuario] = {}
        usuarios[usuario][producto] = {"cantidad": cantidad, "consumo": {}}
        for momento in momentos:
            usuarios[usuario][producto]["consumo"][momento] = int(consumo.get(momento, 0))
        return jsonify({"message": "Producto agregado", "inventario": usuarios[usuario]})
    return jsonify({"error": "Datos inválidos"}), 400

@app.route('/registrar_consumo', methods=['POST'])
def registrar_consumo():
    if 'usuario' not in session:
        return jsonify({"error": "No autenticado"}), 401
    usuario = session['usuario']
    data = request.json
    producto = data.get("producto")
    if usuario in usuarios and producto in usuarios[usuario]:
        total_consumo = sum(usuarios[usuario][producto]["consumo"].values())
        usuarios[usuario][producto]["cantidad"] -= total_consumo
        if usuarios[usuario][producto]["cantidad"] <= 0:
            return jsonify({"warning": f"{producto} se ha agotado. Debes comprar más."})
        return jsonify({"message": "Consumo registrado", "inventario": usuarios[usuario]})
    return jsonify({"error": "Producto no registrado"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
