# Gestor de Notas Estudiantiles

Aplicación web desarrollada en Python para registrar estudiantes, administrar sus calificaciones y calcular automáticamente su promedio académico.

## Funcionalidades

- Registrar estudiantes con tres calificaciones.
- Consultar el listado de estudiantes.
- Editar y eliminar registros (CRUD).
- Calcular el promedio de las tres notas.
- Determinar si el estudiante aprueba (promedio mayor o igual a 3.0) o reprueba.
- Consultar el estudiante con mejor promedio.
- Guardar la información en una base de datos SQLite.

## Tecnologías utilizadas

- **Python:** lógica y procesamiento de datos.
- **Flask:** servidor web y API.
- **HTML, CSS y JavaScript:** interfaz web.
- **SQLite:** almacenamiento persistente de estudiantes.

## Estructura del proyecto

```text
gestor-notas/
├── app.py
├── database.py
├── operaciones.py
├── requirements.txt
├── .gitignore
└── frontend/
    ├── index.html
    ├── styles.css
    └── app.js
```

## Instalación y ejecución

**1.** Descargar o clonar el repositorio.

**2.** Abrir la carpeta del proyecto en Visual Studio Code.

**3.** Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

**4.** Ejecutar la aplicación:

```bash
python app.py
```

**5.** Abrir en el navegador:

http://127.0.0.1:5000

## Base de datos y persistencia

La aplicación utiliza SQLite para almacenar los estudiantes y sus notas.

La base de datos se crea automáticamente en `datos/gestor_notas.db` cuando se inicia el sistema por primera vez.

Los registros permanecen guardados aunque se cierre y vuelva a ejecutar la aplicación.
