import json
from pathlib import Path

RUTA_DATOS = Path(__file__).resolve().parent / "datos_progreso.json"

VOCALES = ("A", "E", "I", "O", "U")


def progreso_inicial():
    return {
        vocal: {
            "estrellas": 0,
            "estado": "Pendiente",
            "intentos": 0,
        }
        for vocal in VOCALES
    }


def cargar_datos():
    """Lee los datos guardados y corrige datos incompletos."""
    if not RUTA_DATOS.exists():
        return None

    try:
        with RUTA_DATOS.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return None

    if not isinstance(datos, dict):
        return None

    progreso = progreso_inicial()
    progreso_guardado = datos.get("progreso", {})

    if isinstance(progreso_guardado, dict):
        for vocal in VOCALES:
            if isinstance(progreso_guardado.get(vocal), dict):
                progreso[vocal].update(progreso_guardado[vocal])

    datos["progreso"] = progreso
    return datos


def guardar_datos(datos):
    """Guarda los datos en formato JSON."""
    with RUTA_DATOS.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def guardar_perfil(nombre, grado, numero):
    """Guarda el perfil sin borrar el progreso anterior."""
    datos = cargar_datos() or {
        "progreso": progreso_inicial()
    }

    datos["perfil_activo"] = {
        "nombre": str(nombre).strip(),
        "grado": grado,
        "numero_lista": numero,
    }

    guardar_datos(datos)
    return datos


def actualizar_progreso(vocal, estrellas):
    """Actualiza el mejor resultado de una vocal."""
    vocal = str(vocal).upper().strip()

    if vocal not in VOCALES:
        return cargar_datos()

    try:
        estrellas = max(0, min(3, int(estrellas)))
    except (TypeError, ValueError):
        estrellas = 0

    datos = cargar_datos() or {
        "progreso": progreso_inicial()
    }

    info = datos["progreso"][vocal]
    info["intentos"] = int(info.get("intentos", 0)) + 1
    info["estrellas"] = max(int(info.get("estrellas", 0)), estrellas)
    info["estado"] = (
        "¡Completado!" if info["estrellas"] == 3 else "En práctica"
    )

    guardar_datos(datos)
    return datos