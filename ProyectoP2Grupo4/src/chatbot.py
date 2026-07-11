"""
chatbot.py

Núcleo del asistente virtual.
Carga las intenciones, construye el modelo TF-IDF
y responde las consultas del usuario.
"""

import json
import os
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocesamiento import preprocesar
from entidades import extraer_entidades

UMBRAL_CONFIANZA_DEFECTO = 0.50

# ruta al json de intenciones, sin importar desde donde se ejecute el script
CARPETA_SRC = os.path.dirname(os.path.abspath(__file__))
RUTA_INTENCIONES = os.path.join(CARPETA_SRC, "..", "data", "intenciones.json")

class AgenteConversacional:
    def __init__(self, ruta_json: str, umbral: float = UMBRAL_CONFIANZA_DEFECTO):
        self.umbral = umbral
        self.respuestas_por_intent = {}
        self.respuestas_fallback = [
            "Lo siento, no entendi tu consulta. ¿Puedes reformularla?"
        ]

        self._cargar_datos(ruta_json)
        self._construir_vectorizador()

    # Carga y preparacion de datos

    def _cargar_datos(self, ruta_json: str) -> None:
        try:
            with open(ruta_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"No se pudo cargar el archivo de intenciones: {e}")

        self.corpus_utterances = []      # frases preprocesadas (para TF-IDF)
        self.corpus_intents = []         # intent asociado a cada fila del corpus

        for item in data.get("intenciones", []):
            intent = item["intent"]
            self.respuestas_por_intent[intent] = item.get("respuestas", [])
            for utterance in item.get("utterances", []):
                self.corpus_utterances.append(preprocesar(utterance))
                self.corpus_intents.append(intent)

        fallback = data.get("fallback", {})
        if fallback.get("respuestas"):
            self.respuestas_fallback = fallback["respuestas"]

        if not self.corpus_utterances:
            raise RuntimeError("El archivo de intenciones no contiene utterances.")

    def _construir_vectorizador(self) -> None:
        # unigramas y bigramas sobre el corpus ya preprocesado
        self.vectorizador = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
        self.matriz_tfidf = self.vectorizador.fit_transform(self.corpus_utterances)

    # Deteccion de intencion

    def detectar_intencion(self, consulta: str):
        """
        Devuelve (intent_detectado, similitud_maxima).
        Si la similitud maxima no supera el umbral, intent_detectado = None.
        """
        consulta_proc = preprocesar(consulta)
        if not consulta_proc:
            return None, 0.0

        vector_consulta = self.vectorizador.transform([consulta_proc])
        similitudes = cosine_similarity(vector_consulta, self.matriz_tfidf)[0]

        idx_max = similitudes.argmax()
        score_max = float(similitudes[idx_max])

        if score_max < self.umbral:
            return None, score_max

        return self.corpus_intents[idx_max], score_max

    # Respuesta al usuario
    def responder(self, consulta: str) -> dict:
        """
        Procesa una consulta de usuario y devuelve un dict con:
        respuesta, intent, similitud y entidades detectadas.
        Maneja entradas problematicas (vacias, no reconocidas) sin detener
        la ejecucion.
        """
        try:
            if not consulta or not consulta.strip():
                return {
                    "respuesta": "Por favor escribe tu consulta, el mensaje llego vacio.",
                    "intent": None,
                    "similitud": 0.0,
                    "entidades": {},
                }

            intent, score = self.detectar_intencion(consulta)
            entidades = extraer_entidades(consulta)

            if intent is None:
                respuesta = random.choice(self.respuestas_fallback)
            else:
                respuesta = random.choice(self.respuestas_por_intent[intent])

            # pequeño uso de las entidades detectadas, para que la
            # respuesta no sea siempre exactamente igual
            if entidades.get("carreras"):
                carrera = entidades["carreras"][0]
                respuesta += f" Vi que mencionaste la carrera de {carrera}, para dudas especificas de esa carrera revisa tambien el portal oficial."

            if entidades.get("cedula"):
                ultimo_digito = entidades["cedula"][0][-1]
                respuesta += f" Segun tu cedula, tu ultimo digito es {ultimo_digito}; revisa el cronograma para ver la fecha que te corresponde."

            return {
                "respuesta": respuesta,
                "intent": intent,
                "similitud": round(score, 3),
                "entidades": entidades,
            }

        except Exception as e:
            # Cualquier error inesperado no debe detener el agente
            return {
                "respuesta": "Ocurrio un problema procesando tu consulta, intenta de nuevo.",
                "intent": None,
                "similitud": 0.0,
                "entidades": {},
                "error": str(e),
            }

agente = AgenteConversacional(RUTA_INTENCIONES)

if __name__ == "__main__":

    while True:

        consulta = input("Tú: ")

        if consulta.lower() == "salir":
            break

        respuesta = agente.responder(consulta)

        print("\nBot:", respuesta["respuesta"])

        print("Intent:", respuesta["intent"])

        print("Similitud:", respuesta["similitud"])

        print("Entidades:", respuesta["entidades"])

        print()