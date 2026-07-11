"""
Limpieza, normalizacion, tokenizacion, eliminacion de stopwords y stemming
para las frases de usuario (utterances) del agente conversacional.
"""

import re
import unicodedata

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# Descarga silenciosa de recursos NLTK necesarios (solo la primera vez)
try:
    stopwords.words("spanish")
except LookupError:
    nltk.download("stopwords", quiet=True)

_STOPWORDS_ES = set(stopwords.words("spanish"))

# palabras interrogativas que NLTK marca como stopword pero que en un
# chatbot de preguntas cortas SI aportan significado (ej. "quien eres")
_PALABRAS_UTILES_PREGUNTAS = {
    "que", "quien", "quienes", "como", "cual", "cuales",
    "cuando", "donde", "cuanto", "cuantos", "cuanta", "cuantas",
}
_STOPWORDS_ES = _STOPWORDS_ES - _PALABRAS_UTILES_PREGUNTAS

_STEMMER = SnowballStemmer("spanish")

# Palabras cortas de chat/whatsapp y errores tipograficos comunes que vimos
# en las pruebas del agente. Se reemplazan por su forma normal ANTES de
# quitar stopwords, para que el vectorizador reconozca la palabra real.
_JERGA_Y_TYPOS = {
    "q": "que",
    "k": "que",
    "xq": "porque",
    "pq": "porque",
    "tb": "tambien",
    "tmb": "tambien",
    "dnd": "donde",
    "x": "por",
    "uni": "universidad",
    "admi": "admision",
    "admicion": "admision",
    "amision": "admision",
    "nesesito": "necesito",
    "nececito": "necesito",
    "komo": "como",
    "kuando": "cuando",
    "grasias": "gracias",
    "graxias": "gracias",
}


def normalizar_jerga(tokens: list) -> list:
    return [_JERGA_Y_TYPOS.get(t, t) for t in tokens]


def quitar_tildes(texto: str) -> str:
    """Elimina acentos/tildes conservando la letra base (ej: 'ó' -> 'o')."""
    nfkd = unicodedata.normalize("NFD", texto)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def limpiar_texto(texto: str) -> str:
    """
    Limpieza y normalizacion basica:
    - minusculas
    - eliminacion de tildes
    - eliminacion de signos de puntuacion y caracteres especiales
    - colapso de espacios multiples
    """
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = quitar_tildes(texto)
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def tokenizar(texto: str) -> list:
    return texto.split()


def quitar_stopwords(tokens: list) -> list:
    return [t for t in tokens if t not in _STOPWORDS_ES and quitar_tildes(t) not in _STOPWORDS_ES]


def aplicar_stemming(tokens: list) -> list:
    return [_STEMMER.stem(t) for t in tokens]


def preprocesar(texto: str, usar_stemming: bool = True) -> str:
    """
    Pipeline completo de preprocesamiento. Devuelve una cadena de tokens
    limpios, sin stopwords y (opcionalmente) con stemming, lista para
    pasar al vectorizador TF-IDF.
    """
    texto_limpio = limpiar_texto(texto)
    tokens = tokenizar(texto_limpio)
    tokens = normalizar_jerga(tokens)
    tokens = quitar_stopwords(tokens)
    if usar_stemming:
        tokens = aplicar_stemming(tokens)
    return " ".join(tokens)

if __name__ == "__main__":

    texto = "¡Hola! ¿Cómo puedo crear mi cuenta en la Universidad?"

    print(preprocesar(texto))