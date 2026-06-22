from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)

# Cargar modelo
modelo = tf.keras.models.load_model("keras_model.h5")

# Cargar etiquetas
with open("labels.txt", "r") as f:
    etiquetas = [line.strip().split(" ", 1)[1] for line in f.readlines()]

    
@app.route("/")
def inicio():
    return "Servidor Beauty AI funcionando"

@app.route("/analizar", methods=["POST"])
def analizar():

    # Verificar que se haya recibido una imagen
    if len(request.files) == 0:
        return jsonify({
            "error": "No se recibió ninguna imagen"
        }), 400

    # Obtener la imagen enviada
    imagen_archivo = list(request.files.values())[0]

    # Abrir y preparar imagen
    imagen = Image.open(imagen_archivo).convert("RGB")
    imagen = imagen.resize((224, 224))

    datos = np.asarray(imagen, dtype=np.float32)
    datos = (datos / 127.5) - 1
    datos = np.expand_dims(datos, axis=0)

    # Predicción
    prediccion = modelo.predict(datos)

    indice = np.argmax(prediccion)
    tono_detectado = etiquetas[indice]

    # Recomendaciones según tono
    if tono_detectado == "Clara":
        recomendaciones = [
            "Rosa pastel",
            "Coral",
            "Nude rosado"
        ]

    elif tono_detectado == "Morena":
        recomendaciones = [
            "Terracota",
            "Vino",
            "Nude cálido"
        ]

    elif tono_detectado == "Obscura":
        recomendaciones = [
            "Borgoña",
            "Ciruela",
            "Rojo intenso"
        ]

    else:
        recomendaciones = [
            "Nude universal",
            "Rojo clásico"
        ]

    return jsonify({
        "tono": tono_detectado,
        "labiales": recomendaciones
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
