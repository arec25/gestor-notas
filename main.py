"""Gestor de Notas Estudiantiles - programa principal."""

import csv
import os

from operaciones import calcular_promedio, estado, mejor_estudiante, nota_valida

ARCHIVO = os.path.join(os.path.dirname(__file__), "datos", "estudiantes.csv")


def cargar_estudiantes():
    estudiantes = []
    if not os.path.exists(ARCHIVO):
        return estudiantes
    with open(ARCHIVO, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            notas = [float(fila["nota1"]), float(fila["nota2"]), float(fila["nota3"])]
            estudiantes.append({"nombre": fila["nombre"], "notas": notas})
    return estudiantes


def guardar_estudiantes(estudiantes):
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["nombre", "nota1", "nota2", "nota3"])
        for e in estudiantes:
            escritor.writerow([e["nombre"], *e["notas"]])
    print("Cambios guardados correctamente.")


def mostrar_estudiantes(estudiantes):
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
    print(f"\n{'Nombre':<20}{'Promedio':>10}   Estado")
    print("-" * 42)
    for e in estudiantes:
        prom = calcular_promedio(e["notas"])
        print(f"{e['nombre']:<20}{prom:>10.2f}   {estado(prom)}")


def pedir_nota(numero):
    while True:
        try:
            nota = float(input(f"Nota {numero} (0.0 - 5.0): "))
            if nota_valida(nota):
                return nota
            print("La nota debe estar entre 0.0 y 5.0.")
        except ValueError:
            print("Escribe un número válido, por ejemplo 3.5")


def agregar_estudiante(estudiantes):
    nombre = input("Nombre del estudiante: ").strip()
    if not nombre:
        print("El nombre no puede estar vacío.")
        return
    notas = [pedir_nota(i) for i in range(1, 4)]
    estudiantes.append({"nombre": nombre, "notas": notas})
    print(f"{nombre} agregado con promedio {calcular_promedio(notas):.2f}")


def mostrar_mejor(estudiantes):
    mejor = mejor_estudiante(estudiantes)
    if mejor:
        print(f"Mejor promedio: {mejor['nombre']} con {calcular_promedio(mejor['notas']):.2f}")
    else:
        print("No hay estudiantes registrados.")


def menu():
    estudiantes = cargar_estudiantes()
    while True:
        print("\n=== GESTOR DE NOTAS ===")
        print("1. Ver estudiantes")
        print("2. Agregar estudiante")
        print("3. Ver mejor promedio")
        print("4. Guardar cambios")
        print("5. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            mostrar_estudiantes(estudiantes)
        elif opcion == "2":
            agregar_estudiante(estudiantes)
        elif opcion == "3":
            mostrar_mejor(estudiantes)
        elif opcion == "4":
            guardar_estudiantes(estudiantes)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
