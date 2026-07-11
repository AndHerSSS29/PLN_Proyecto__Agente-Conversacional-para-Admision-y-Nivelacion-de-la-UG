# Agente Conversacional para Admisión y Nivelación de la UG

Trabajo Parcial II - Procesamiento de Lenguaje Natural
Universidad de Guayaquil - Carrera de Ciencia de Datos & IA

## Objetivo

Chatbot que responde preguntas frecuentes sobre admisión y nivelación de la
Universidad de Guayaquil (y algo de información general de la universidad:
historia, misión/visión, facultades, ubicación, redes sociales), usando
técnicas clásicas de PLN (TF-IDF + similitud coseno para detectar la
intención del usuario y devolver una respuesta predefinida). No usa deep
learning ni modelos generativos.

## Estructura del repositorio

```
chatbot/
├── data/
│   └── intenciones.json     # intenciones, utterances y respuestas
├── src/
│   ├── preprocesamiento.py  # limpieza, tokenizacion, stopwords, stemming
│   ├── entidades.py         # extraccion de entidades con regex
│   ├── chatbot.py           # TF-IDF, similitud coseno, deteccion de intencion y fallback
│   ├── evaluacion.py        # pruebas del agente y calculo de accuracy
│   ├── app.py                # servidor Flask (interfaz web)
│   ├── templates/index.html
│   └── static/               # css, js, imagen del logo
├── requirements.txt
└── README.md
```

## Cómo ejecutarlo

1. Instalar dependencias:
```
pip install -r requirements.txt
```

2. Opción consola (sin interfaz web):
```
cd src
python chatbot.py
```
Escribe tu consulta y presiona enter. Escribe "salir" para terminar.

3. Opción web (Flask):
```
cd src
python app.py
```
Luego abrir el navegador en `http://127.0.0.1:5000/`.

4. Correr la evaluación del agente:
```
cd src
python evaluacion.py
```
Esto corre 27 consultas de prueba (parafraseos, errores tipográficos y
preguntas fuera de alcance) e imprime el accuracy y una breve discusión de
las limitaciones observadas.

## Notas

- El umbral de confianza para el fallback está en `chatbot.py`
  (`UMBRAL_CONFIANZA_DEFECTO = 0.50`).
- Las intenciones, utterances y respuestas están en `data/intenciones.json`,
  separado del código, para poder editarlas sin tocar la lógica del agente.
- La primera vez que se ejecuta, `preprocesamiento.py` descarga las
  stopwords de NLTK en español (requiere conexión a internet esa vez).
