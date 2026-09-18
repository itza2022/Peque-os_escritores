# Documentación interna de la lógica de la app

## 1. Objetivo general
La aplicación está diseñada para ayudar a niños a practicar la escritura de vocales en una pantalla táctil. Cada vocal tiene un estado de progreso y se guarda en un archivo JSON para que el docente pueda revisarlo después.

---

## 2. Estructura principal

### main.py
Es el archivo central de navegación.

Función principal:
- crea la pantalla del formulario
- crea el ScreenManager
- gestiona el cambio entre pantallas:
  - formulario
  - menú de vocales
  - lienzo de trazo
  - reporte

Métodos relevantes:
- build()
  - inicializa la aplicación
  - agrega la primera pantalla
- ir_a_menu(datos=None)
  - mueve al usuario al menú
- ir_a_lienzo(vocal)
  - abre el lienzo de la vocal seleccionada
- ir_a_reporte()
  - abre la pantalla del reporte
- volver_al_menu()
  - vuelve al menú principal

---

## 3. Formulario de registro

### formulario.py
Aquí el alumno registra sus datos:

- nombre
- grado/sección
- número en lista

Flujo:
1. el usuario llena los campos
2. presiona “Guardar e Iniciar”
3. se llama a guardar_perfil(nombre, grado, numero)
4. la app guarda el perfil activo en JSON
5. se ejecuta el callback para ir al menú

Importante:
- el callback que recibe la clase es al_completar_callback
- desde main.py se le pasa self.ir_a_menu

---

## 4. Menú de vocales

### menu_vocales.py
Muestra cinco opciones:

- A
- E
- I
- O
- U

Cada botón tiene un callback:
- al_seleccionar_vocal(vocal) → abre el lienzo de esa vocal
- al_ver_reporte() → abre la vista del reporte

El menú no guarda datos directamente; solo dispara navegación.

---

## 5. Lienzo de trazado

### lienzo_trazado.py
Aquí se dibuja la vocal.

Clases:
- RielesLienzo
  - dibuja fondo con franjas de color
  - recibe los toques del usuario
  - registra los puntos del trazo
- PantallaLienzo
  - crea el área de dibujo
  - agrega botones: Borrar y Listo
  - al guardar, evalúa la calidad del trazo

Flujo:
1. on_touch_down
   - empieza una línea en el punto donde toca
   - inicia la lista de puntos
2. on_touch_move
   - agrega más puntos mientras arrastra
3. on_touch_up
   - finaliza el trazo
4. evaluar_trazo()
   - calcula si el dibujo es válido
5. guardar_y_volver()
   - llama a actualizar_progreso(vocal, estrellas)
   - vuelve al menú

Validación lógica:
- si el trazo tiene pocos puntos, se considera débil
- si ocupa más ancho/alto y tiene trayectoria suficiente, gana más estrellas
- si es solo un toque, se marca como intento pobre o no válido

---

## 6. Persistencia de datos

### gestor_datos.py
Este módulo guarda y lee el progreso en:

- datos_progreso.json

Estructura principal:
```python
{
  "perfil_activo": {
    "nombre": "...",
    "grado": "...",
    "numero_lista": 1
  },
  "progreso": {
    "A": {
      "estrellas": 2,
      "estado": "En práctica",
      "intentos": 4
    },
    "E": {
      "estrellas": 0,
      "estado": "Pendiente",
      "intentos": 0
    }
  }
}
```

Funciones clave:
- progreso_inicial()
  - crea el formato base para cada vocal
- cargar_datos()
  - carga los datos guardados
  - corrige estructuras incompletas
- guardar_datos(datos)
  - escribe el JSON
- guardar_perfil(nombre, grado, numero)
  - guarda el perfil activo
- actualizar_progreso(vocal, estrellas)
  - incrementa intentos
  - actualiza estrellas
  - pone el estado de la vocal

---

## 7. Reporte

### reporte.py
Muestra el progreso del alumno.

Función:
- lee los datos del JSON
- presenta:
  - nombre del alumno
  - grado
  - número de lista
  - estado de cada vocal
  - estrellas acumuladas
  - número de intentos

Importante:
- la vista se reconstruye cada vez que entra a la pantalla con on_pre_enter
- esto garantiza que el docente vea siempre la información actualizada

---

## Flujo completo de la lógica
1. El alumno registra sus datos
2. Selecciona una vocal
3. Dibuja en el lienzo
4. El sistema evalúa el trazo
5. Se guarda el progreso en JSON
6. El docente revisa el reporte
7. El reporte se actualiza dinámicamente con los datos reales

---

## Regla importante para no romper el flujo
Cada vez que se modifique código:
- no cambiar nombres de clase sin corregir imports
- no cambiar nombres de callback sin actualizar llamadas
- no cambiar el nombre del JSON sin actualizar cargar_datos y guardar_datos
- usar siempre la venv del proyecto para ejecutar la app
