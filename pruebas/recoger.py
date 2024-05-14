from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

# Función para generar una cantidad especificada de DNIs aleatorios
def generar_dniss(cantidad):
    dniss = []  # Lista para almacenar los DNIs generados
    for _ in range(cantidad):
        # Código para generar un número de DNI aleatorio
        dni = "12345678A"  # Este es solo un ejemplo, reemplázalo con tu propia lógica de generación de DNIs
        dniss.append(dni)
    return dniss

# Ruta para generar DNIs con una cantidad especificada
@app.route('/codigo', methods=['GET', 'POST'])
def generar_codigos():
    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        dniss = generar_dniss(cantidad)
        return jsonify({'dniss': dniss})
    else:
        return "Método GET no permitido en esta ruta", 405
if __name__ == '__main__':
    app.run(debug=True)