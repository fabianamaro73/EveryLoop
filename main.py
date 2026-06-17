from flask import Flask, request, jsonify

app = Flask(__name__)

# Página principal
@app.route("/")
def inicio():
    return "Servidor Beauty AI funcionando"

# Ruta para analizar imágenes
@app.route("/analizar", methods=["POST"])
def analizar():

    # Aquí recibiremos la foto
    imagen = request.files['file']

    # Resultado temporal
    tono_detectado = "Morena"

    recomendaciones = [
        "Terracota",
        "Vino",
        "Nude cálido"
    ]

    return jsonify({
        "tono": tono_detectado,
        "labiales": recomendaciones
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)