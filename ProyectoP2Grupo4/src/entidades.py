"""
Extraccion de entidades del dominio mediante reglas y expresiones regulares.
RF-05: Extraccion de entidades
"""

import re
from preprocesamiento import quitar_tildes

# Lista de carreras UG frecuentemente mencionadas
_CARRERAS = [
    "ciencia de datos e inteligencia artificial",
    "ciencia de datos",
    "ingenieria en sistemas",
    "ingenieria civil",
    "medicina",
    "derecho",
    "psicologia",
    "administracion de empresas",
    "contaduria publica",
    "arquitectura",
    "enfermeria",
    "odontologia",
]

# Terminos especificos del proceso (dominio) a detectar tal cual aparecen
_TERMINOS_DOMINIO = [
    "curso de nivelacion",
    "cupo aceptado",
    "cupo",
    "matricula ordinaria",
    "matricula",
    "cronograma de registro",
    "cronograma",
    "cuenta de aspirante",
    "creacion de cuenta",
]

# Fechas: dd/mm/yyyy, dd-mm-yyyy, "10 de julio de 2026", "10 de julio"
_PATRON_FECHA_NUMERICA = r"\b\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?\b"
_MESES = (
    "enero|febrero|marzo|abril|mayo|junio|julio|agosto|"
    "septiembre|setiembre|octubre|noviembre|diciembre"
)
_PATRON_FECHA_TEXTO = rf"\b\d{{1,2}}\s+de\s+(?:{_MESES})(?:\s+de\s+\d{{4}})?\b"

# Cedula ecuatoriana: 10 digitos consecutivos
_PATRON_CEDULA = r"\b\d{10}\b"


def extraer_fechas(texto: str) -> list:
    fechas = re.findall(_PATRON_FECHA_TEXTO, texto, flags=re.IGNORECASE)
    fechas += re.findall(_PATRON_FECHA_NUMERICA, texto)
    return fechas


def extraer_cedula(texto: str) -> list:
    return re.findall(_PATRON_CEDULA, texto)


def extraer_carreras(texto: str) -> list:
    texto = quitar_tildes(texto.lower())
    return [c for c in _CARRERAS if c in texto]


def extraer_terminos_dominio(texto: str) -> list:
    texto = quitar_tildes(texto.lower())
    encontrados = []
    for termino in _TERMINOS_DOMINIO:
        if termino in texto and termino not in encontrados:
            encontrados.append(termino)
    return encontrados


def extraer_entidades(texto: str) -> dict:
    """Extrae todas las entidades soportadas de un texto crudo (sin preprocesar)."""
    return {
        "fechas": extraer_fechas(texto),
        "cedula": extraer_cedula(texto),
        "carreras": extraer_carreras(texto),
        "terminos_dominio": extraer_terminos_dominio(texto),
    }

if __name__ == "__main__":

    texto = "Mi cédula es 0912345678 y quiero estudiar Ingeniería Civil el 10 de julio."

    print(extraer_entidades(texto))