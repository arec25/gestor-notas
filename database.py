"""Persistencia de estudiantes en SQLite para la aplicación web."""

import os
import sqlite3
from contextlib import closing
from pathlib import Path

from operaciones import calcular_promedio, estado, mejor_estudiante

BASE = Path(__file__).resolve().parent
RUTA_DB = Path(os.environ.get("GESTOR_DB_PATH", str(BASE / "datos" / "gestor_notas.db")))


def conectar():
    conexion = sqlite3.connect(RUTA_DB, timeout=10)
    conexion.row_factory = sqlite3.Row
    return conexion


def iniciar_base_datos():
    """Crea la base de datos vacía y su tabla al ejecutar la aplicación por primera vez."""
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)
    with closing(conectar()) as conexion:
        with conexion:
            conexion.execute(
                """CREATE TABLE IF NOT EXISTS estudiantes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    nota1 REAL NOT NULL CHECK (nota1 BETWEEN 0 AND 5),
                    nota2 REAL NOT NULL CHECK (nota2 BETWEEN 0 AND 5),
                    nota3 REAL NOT NULL CHECK (nota3 BETWEEN 0 AND 5)
                )"""
            )


def _como_diccionario(fila):
    notas = [fila["nota1"], fila["nota2"], fila["nota3"]]
    promedio = calcular_promedio(notas)
    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "notas": notas,
        "promedio": promedio,
        "estado": estado(promedio),
    }


def listar_estudiantes():
    with closing(conectar()) as conexion:
        filas = conexion.execute(
            "SELECT id, nombre, nota1, nota2, nota3 FROM estudiantes ORDER BY id"
        ).fetchall()
    return [_como_diccionario(fila) for fila in filas]


def obtener_estudiante(estudiante_id):
    with closing(conectar()) as conexion:
        fila = conexion.execute(
            "SELECT id, nombre, nota1, nota2, nota3 FROM estudiantes WHERE id = ?",
            (estudiante_id,),
        ).fetchone()
    return _como_diccionario(fila) if fila is not None else None


def crear_estudiante(nombre, notas):
    with closing(conectar()) as conexion:
        with conexion:
            cursor = conexion.execute(
                "INSERT INTO estudiantes (nombre, nota1, nota2, nota3) VALUES (?, ?, ?, ?)",
                (nombre, *notas),
            )
            estudiante_id = cursor.lastrowid
    return obtener_estudiante(estudiante_id)


def actualizar_estudiante(estudiante_id, nombre, notas):
    with closing(conectar()) as conexion:
        with conexion:
            cursor = conexion.execute(
                "UPDATE estudiantes SET nombre=?, nota1=?, nota2=?, nota3=? WHERE id=?",
                (nombre, *notas, estudiante_id),
            )
    return obtener_estudiante(estudiante_id) if cursor.rowcount else None


def eliminar_estudiante(estudiante_id):
    with closing(conectar()) as conexion:
        with conexion:
            cursor = conexion.execute(
                "DELETE FROM estudiantes WHERE id=?", (estudiante_id,)
            )
    return cursor.rowcount > 0


def obtener_estadisticas():
    estudiantes = listar_estudiantes()
    mejor = mejor_estudiante(estudiantes)
    return {
        "total": len(estudiantes),
        "aprobados": sum(e["estado"] == "Aprobado" for e in estudiantes),
        "reprobados": sum(e["estado"] == "Reprobado" for e in estudiantes),
        "mejor_estudiante": mejor,
    }
