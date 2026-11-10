"""Interfaz web y API REST del Gestor de Notas Estudiantiles."""

import math
import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from database import (
    actualizar_estudiante,
    crear_estudiante,
    eliminar_estudiante,
    iniciar_base_datos,
    listar_estudiantes,
    obtener_estadisticas,
    obtener_estudiante,
)
from operaciones import nota_valida

app = Flask(__name__)
FRONTEND = Path(__file__).resolve().parent / "frontend"

# Una vez creada, la base SQLite conserva los registros entre reinicios.
iniciar_base_datos()


def validar_datos(datos):
    """Devuelve (nombre, notas, error) tras validar la entrada."""
    if not isinstance(datos, dict):
        return None, None, "Envía los datos del estudiante en formato JSON."

    nombre = datos.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        return None, None, "El nombre del estudiante es obligatorio."
    nombre = nombre.strip()
    if len(nombre) > 100:
        return None, None, "El nombre no puede superar 100 caracteres."

    valores = datos.get("notas")
    if not isinstance(valores, list) or len(valores) != 3:
        return None, None, "Debes ingresar exactamente tres notas."

    notas = []
    for indice, valor in enumerate(valores, start=1):
        if isinstance(valor, bool) or valor is None:
            return None, None, f"La nota {indice} no es válida."
        try:
            numero = float(valor)
        except (ValueError, TypeError):
            return None, None, f"La nota {indice} debe ser un número."
        if not math.isfinite(numero) or not nota_valida(numero):
            return None, None, f"La nota {indice} debe estar entre 0 y 5."
        notas.append(numero)

    return nombre, notas, None


@app.get("/")
def inicio():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/styles.css")
def estilos():
    return send_from_directory(FRONTEND, "styles.css")


@app.get("/app.js")
def javascript():
    return send_from_directory(FRONTEND, "app.js")


@app.get("/api/health")
def estado_api():
    return jsonify({"estado": "ok", "servicio": "Gestor de Notas API"})


@app.get("/api/estudiantes")
def listar():
    return jsonify(listar_estudiantes())


@app.get("/api/estudiantes/<int:estudiante_id>")
def consultar(estudiante_id):
    estudiante = obtener_estudiante(estudiante_id)
    if estudiante is None:
        return jsonify({"error": "Estudiante no encontrado."}), 404
    return jsonify(estudiante)


@app.post("/api/estudiantes")
def agregar():
    nombre, notas, error = validar_datos(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400
    return jsonify(crear_estudiante(nombre, notas)), 201


@app.put("/api/estudiantes/<int:estudiante_id>")
def modificar(estudiante_id):
    nombre, notas, error = validar_datos(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400
    estudiante = actualizar_estudiante(estudiante_id, nombre, notas)
    if estudiante is None:
        return jsonify({"error": "Estudiante no encontrado."}), 404
    return jsonify(estudiante)


@app.delete("/api/estudiantes/<int:estudiante_id>")
def borrar(estudiante_id):
    if not eliminar_estudiante(estudiante_id):
        return jsonify({"error": "Estudiante no encontrado."}), 404
    return jsonify({"mensaje": "Estudiante eliminado correctamente."})


@app.get("/api/estadisticas")
def estadisticas():
    return jsonify(obtener_estadisticas())


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", "5000"))
    # El host 0.0.0.0 permite usar la misma app más adelante dentro de Docker.
    app.run(host="0.0.0.0", port=puerto, debug=False)
