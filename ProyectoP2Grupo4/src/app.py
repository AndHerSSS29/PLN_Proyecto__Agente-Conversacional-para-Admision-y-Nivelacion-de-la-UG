from flask import Flask, render_template, request, jsonify
from chatbot import agente

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/preguntar", methods=["POST"])
def preguntar():
    datos = request.get_json()
    pregunta = datos.get("mensaje", "")
    respuesta = agente.responder(pregunta)
    return jsonify(respuesta)

if __name__ == "__main__":
    app.run(debug=True)