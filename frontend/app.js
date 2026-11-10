"use strict";

// Las rutas relativas /api también funcionarán cuando Nginx actúe como proxy.
const API = "/api";
let estudiantes = [];
let editandoId = null;

const $ = (id) => document.getElementById(id);
const tabla = $("tabla");
const formulario = $("formulario");

function mostrarMensaje(texto, tipo = "success") {
  const mensaje = $("mensaje");
  mensaje.textContent = texto;
  mensaje.className = `message ${tipo}`;
}

function limpiarMensaje() {
  $("mensaje").className = "message hidden";
  $("mensaje").textContent = "";
}

async function solicitar(ruta, opciones = {}) {
  const respuesta = await fetch(API + ruta, opciones);
  const datos = await respuesta.json().catch(() => ({}));
  if (!respuesta.ok) {
    throw new Error(datos.error || `Error HTTP ${respuesta.status}`);
  }
  return datos;
}

function celda(texto, clase = "") {
  const td = document.createElement("td");
  td.textContent = texto;
  if (clase) td.className = clase;
  return td;
}

function renderizarEstudiantes() {
  const consulta = $("buscar").value.trim().toLocaleLowerCase();
  const filtrados = estudiantes.filter((e) => e.nombre.toLocaleLowerCase().includes(consulta));
  tabla.replaceChildren();
  $("conteo-tabla").textContent = `${filtrados.length} estudiante${filtrados.length === 1 ? "" : "s"}`;

  if (!filtrados.length) {
    const fila = document.createElement("tr");
    const vacia = celda(consulta ? "No encontramos estudiantes con ese nombre." : "No hay estudiantes registrados.", "empty-state");
    vacia.colSpan = 5;
    fila.append(vacia);
    tabla.append(fila);
    return;
  }

  for (const estudiante of filtrados) {
    const fila = document.createElement("tr");
    fila.append(celda(estudiante.nombre));
    fila.append(celda(estudiante.notas.map((nota) => Number(nota).toFixed(1)).join("  ·  "), "grade-list"));
    fila.append(celda(estudiante.promedio.toFixed(2), "average"));

    const estadoCelda = document.createElement("td");
    const estado = document.createElement("span");
    estado.className = `status ${estudiante.estado.toLowerCase()}`;
    estado.textContent = estudiante.estado;
    estadoCelda.append(estado);
    fila.append(estadoCelda);

    const accionesCelda = document.createElement("td");
    const acciones = document.createElement("div");
    acciones.className = "actions";

    const editar = document.createElement("button");
    editar.type = "button";
    editar.className = "action-btn";
    editar.textContent = "Editar";
    editar.addEventListener("click", () => iniciarEdicion(estudiante));

    const eliminar = document.createElement("button");
    eliminar.type = "button";
    eliminar.className = "action-btn delete";
    eliminar.textContent = "Eliminar";
    eliminar.addEventListener("click", () => borrarEstudiante(estudiante));

    acciones.append(editar, eliminar);
    accionesCelda.append(acciones);
    fila.append(accionesCelda);
    tabla.append(fila);
  }
}

async function cargarDatos() {
  try {
    const [lista, resumen] = await Promise.all([
      solicitar("/estudiantes"),
      solicitar("/estadisticas"),
    ]);
    estudiantes = lista;
    $("total").textContent = resumen.total;
    $("aprobados").textContent = resumen.aprobados;
    $("reprobados").textContent = resumen.reprobados;
    $("mejor").textContent = resumen.mejor_estudiante
      ? `Mejor promedio: ${resumen.mejor_estudiante.nombre} (${resumen.mejor_estudiante.promedio.toFixed(2)})`
      : "Mejor promedio: —";
    renderizarEstudiantes();
  } catch (error) {
    mostrarMensaje(`No pudimos consultar la API: ${error.message}`, "error");
    tabla.replaceChildren();
    const fila = document.createElement("tr");
    const celdaError = celda("No se pudo cargar la lista. Revisa que Python esté ejecutándose.", "empty-state");
    celdaError.colSpan = 5;
    fila.append(celdaError);
    tabla.append(fila);
  }
}

function reiniciarFormulario() {
  editandoId = null;
  formulario.reset();
  $("titulo-formulario").textContent = "Nuevo estudiante";
  $("guardar").textContent = "Registrar estudiante →";
  $("cancelar").classList.add("hidden");
}

function iniciarEdicion(estudiante) {
  editandoId = estudiante.id;
  $("nombre").value = estudiante.nombre;
  estudiante.notas.forEach((nota, indice) => { $(`nota${indice + 1}`).value = nota; });
  $("titulo-formulario").textContent = "Editar estudiante";
  $("guardar").textContent = "Guardar cambios →";
  $("cancelar").classList.remove("hidden");
  limpiarMensaje();
  $("nombre").focus();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function borrarEstudiante(estudiante) {
  if (!window.confirm(`¿Eliminar a ${estudiante.nombre}? Esta acción no se puede deshacer.`)) return;
  try {
    await solicitar(`/estudiantes/${estudiante.id}`, { method: "DELETE" });
    if (editandoId === estudiante.id) reiniciarFormulario();
    mostrarMensaje("Estudiante eliminado correctamente.");
    await cargarDatos();
  } catch (error) {
    mostrarMensaje(error.message, "error");
  }
}

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  limpiarMensaje();
  const nombre = $("nombre").value.trim();
  const valores = [$("nota1").value, $("nota2").value, $("nota3").value];
  const notas = valores.map(Number);
  if (!nombre) return mostrarMensaje("Ingresa el nombre del estudiante.", "error");
  if (valores.some((valor) => !valor.trim()) || notas.some((nota) => !Number.isFinite(nota) || nota < 0 || nota > 5)) {
    return mostrarMensaje("Ingresa tres notas válidas entre 0 y 5.", "error");
  }

  const guardar = $("guardar");
  guardar.disabled = true;
  try {
    const editando = editandoId !== null;
    await solicitar(editando ? `/estudiantes/${editandoId}` : "/estudiantes", {
      method: editando ? "PUT" : "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, notas }),
    });
    reiniciarFormulario();
    mostrarMensaje(editando ? "Estudiante actualizado correctamente." : "Estudiante registrado correctamente.");
    await cargarDatos();
  } catch (error) {
    mostrarMensaje(error.message, "error");
  } finally {
    guardar.disabled = false;
  }
});

$("cancelar").addEventListener("click", () => { reiniciarFormulario(); limpiarMensaje(); });
$("buscar").addEventListener("input", renderizarEstudiantes);
cargarDatos();
