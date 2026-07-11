"""
evaluacion.py

RF-08: Evaluacion del agente.
Corre un conjunto de consultas de prueba (parafraseos, errores tipograficos
y preguntas fuera de alcance) contra el agente y calcula el accuracy y el
F1-macro de deteccion de intencion.
"""

from sklearn.metrics import classification_report, accuracy_score

from chatbot import agente

# cada caso es (consulta, intent_esperado)
# se usa None cuando la consulta deberia caer en fallback (no reconocida)
CASOS_PRUEBA = [
    # parafraseos normales, uno por cada intencion
    ("hola buenas", "saludo"),
    ("bueno me despido, gracias", "despedida"),
    ("muy amable, gracias por la informacion", "agradecimiento"),
    ("que necesito para poder inscribirme en la universidad", "preguntar_requisitos_admision"),
    ("como hago para sacar mi cuenta de aspirante", "explicar_creacion_cuenta"),
    ("para cuando es el registro de aspirantes", "consultar_fechas_registro"),
    ("hasta que fecha puedo matricularme", "consultar_cronograma_matricula"),
    ("de que se trata el curso de nivelacion", "preguntar_curso_nivelacion"),
    ("cual es la nota para pasar nivelacion", "consultar_aprobacion_asignaturas"),
    ("donde puedo ver mis notas", "consultar_calificaciones"),
    ("cuantas faltas se permiten en nivelacion", "consultar_control_asistencia"),
    ("todavia hay cupos disponibles", "consultar_cupos"),
    ("quiero estudiar ingenieria en sistemas", "consultar_aceptacion_carrera"),
    ("que papeles necesito escanear para inscribirme", "preguntar_documentos_necesarios"),
    ("en que redes sociales puedo preguntar mis dudas", "consultar_canales_contacto"),
    # variaciones con errores tipograficos
    ("q nesesito para la admicion", "preguntar_requisitos_admision"),
    ("komo creo mi cuenta", "explicar_creacion_cuenta"),
    ("kuando es la matricula", "consultar_cronograma_matricula"),
    ("q pasa si falto mucho a nivelacion", "consultar_control_asistencia"),
    ("tengo cupo aceptado", "consultar_cupos"),
    ("grasias", "agradecimiento"),
    # preguntas ambiguas o fuera de alcance, se espera fallback
    ("cual es el clima en guayaquil", None),
    ("quien es el rector de la universidad", None),
    ("asdkjaskjd", None),
    ("cuanto cuesta la carrera", None),
    ("hola quiero saber si hay clases de guitarra", None),
    ("ayuda", "mostrar_ayuda"),
    ("que puedes hacer", "mostrar_ayuda"),
]


def ejecutar_evaluacion():
    aciertos = 0
    resultados = []

    for consulta, esperado in CASOS_PRUEBA:
        respuesta = agente.responder(consulta)
        obtenido = respuesta["intent"]
        correcto = obtenido == esperado
        if correcto:
            aciertos += 1
        resultados.append((consulta, esperado, obtenido, respuesta["similitud"], correcto))

    total = len(CASOS_PRUEBA)
    accuracy = aciertos / total

    print("=" * 70)
    print("EVALUACION DEL AGENTE - deteccion de intencion")
    print("=" * 70)
    for consulta, esperado, obtenido, sim, correcto in resultados:
        marca = "OK   " if correcto else "FALLO"
        print(f"[{marca}] '{consulta}'")
        print(f"        esperado={esperado}  obtenido={obtenido}  similitud={sim}")

    print("-" * 70)
    print(f"Aciertos: {aciertos}/{total}")
    print(f"Accuracy: {accuracy:.2f}")

    # F1-macro por intencion, usando "fallback" como etiqueta cuando
    # se esperaba o se obtuvo None
    y_esperado = [e if e is not None else "fallback" for _, e, _, _, _ in resultados]
    y_obtenido = [o if o is not None else "fallback" for _, _, o, _, _ in resultados]

    print("-" * 70)
    print("Reporte por intencion (precision, recall, f1):")
    print(classification_report(y_esperado, y_obtenido, zero_division=0))

    print("-" * 70)
    print("Limitaciones observadas:")
    print("- Los intents de charla (saludo, despedida, agradecimiento) usan")
    print("  frases muy cortas y parecidas entre si, por lo que TF-IDF a veces")
    print("  confunde una intencion con otra.")
    print("- Errores tipograficos con varias letras cambiadas (ej. 'nesesito',")
    print("  'admicion') bajan mucho la similitud porque ni el stemmer ni el")
    print("  vectorizador reconocen esas variantes, y la consulta cae en fallback")
    print("  aunque el umbral (0.5) sea razonable para el resto de casos.")
    print("- Preguntas fuera del dominio (costos, clima, temas no relacionados)")
    print("  a veces comparten palabras con el corpus (ej. 'carrera', 'hola') y")
    print("  el agente responde con una intencion incorrecta en vez de fallback.")

    return accuracy


if __name__ == "__main__":
    ejecutar_evaluacion()
