"""Funciones de cálculo para el gestor de notas (conservadas del proyecto original)."""

NOTA_MINIMA = 3.0


def calcular_promedio(notas):
    """Devuelve el promedio de una lista de notas, redondeado a 2 decimales."""
    if not notas:
        return 0.0
    return round(sum(notas) / len(notas), 2)


def estado(promedio):
    """Indica si el estudiante aprueba o reprueba."""
    return "Aprobado" if promedio >= NOTA_MINIMA else "Reprobado"


def mejor_estudiante(estudiantes):
    """Devuelve el estudiante con el promedio más alto."""
    if not estudiantes:
        return None
    return max(estudiantes, key=lambda e: calcular_promedio(e["notas"]))


def nota_valida(nota):
    """Verifica que la nota esté entre 0.0 y 5.0."""
    return 0.0 <= nota <= 5.0
